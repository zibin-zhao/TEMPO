# chip_four_wells.py
# pip install opencv-python numpy
import cv2 as cv, numpy as np, json, sys
from dataclasses import dataclass, asdict

# ----- Canonical canvas and four ROIs (normalized) -----
CANVAS = (1500, 900)  # (H, W) after warp

ROIS = {  # tweak these once from a good reference
    "upper_left":  {"cx": 0.30, "cy": 0.30, "r": 0.075},
    "upper_right": {"cx": 0.70, "cy": 0.30, "r": 0.075},
    "lower_left":  {"cx": 0.30, "cy": 0.70, "r": 0.075},
    "lower_right": {"cx": 0.70, "cy": 0.70, "r": 0.075},
}

# ----- thresholds -----
RATIO_HI = 4.0      # A/B > 4  -> "10"
RATIO_LO = 0.25     # A/B < .25 -> "01"
V_BLACK  = 0.12     # both V < 0.12 -> "00"
GREEN_FLOOR = 1e-3
EPS = 1e-6

@dataclass
class PairResult:
    left: float
    right: float
    ratio: float
    code: str
    row_name: str

# ---------- helpers ----------
def read_image(path):
    buf = np.fromfile(path, dtype=np.uint8)
    img = cv.imdecode(buf, cv.IMREAD_COLOR)
    if img is None: raise ValueError(f"Cannot read {path}")
    return img

def rectify(img):
    """Warp largest quadrilateral to CANVAS; fallback to resize."""
    H,W = CANVAS
    g = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    g = cv.GaussianBlur(g,(5,5),0)
    edges = cv.Canny(g,50,150)
    cnts,_ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if not cnts: return cv.resize(img,(W,H))
    cnt = max(cnts, key=cv.contourArea)
    peri = cv.arcLength(cnt, True)
    approx = cv.approxPolyDP(cnt, 0.02*peri, True)
    if len(approx) != 4: return cv.resize(img,(W,H))
    pts = approx.reshape(-1,2).astype(np.float32)
    s = pts.sum(1); d = np.diff(pts, axis=1).ravel()
    ordered = np.array([pts[np.argmin(s)], pts[np.argmin(d)],
                        pts[np.argmax(s)], pts[np.argmax(d)]], np.float32)
    dst = np.array([[0,0],[W-1,0],[W-1,H-1],[0,H-1]], np.float32)
    M = cv.getPerspectiveTransform(ordered, dst)
    return cv.warpPerspective(img, M, (W, H))

def roi_mask(shape, cx, cy, r):
    H,W = shape
    x = int(cx*W); y = int(cy*H); rad = max(2, int(r*W)-2)
    m = np.zeros((H,W), np.uint8); cv.circle(m,(x,y),rad,255,-1); return m

def measure(img, key):
    """Return (greenness in [0,1], brightness V in [0,1]) for ROI."""
    H,W = img.shape[:2]
    m = roi_mask((H,W), ROIS[key]["cx"], ROIS[key]["cy"], ROIS[key]["r"])
    pix = img[m>0].astype(np.float32)
    if pix.size == 0: return 0.0, 0.0
    B,G,R = pix[:,0], pix[:,1], pix[:,2]
    denom = R+G+B+EPS
    green = float(np.mean(np.maximum(0.0, G - np.maximum(R,B)) / denom))
    V = cv.cvtColor(img, cv.COLOR_BGR2HSV)[:,:,2][m>0] / 255.0
    return green, float(np.mean(V))

def decide(A, Va, B, Vb):
    if Va < V_BLACK and Vb < V_BLACK: return 0.0, "00"
    ratio = (A+GREEN_FLOOR) / (B+GREEN_FLOOR)
    if ratio > RATIO_HI: return ratio, "10"
    if ratio < RATIO_LO: return ratio, "01"
    return ratio, "11"

def save_debug(img, path):
    H,W = img.shape[:2]
    vis = img.copy()
    for name,p in ROIS.items():
        x=int(p["cx"]*W); y=int(p["cy"]*H); r=max(2,int(p["r"]*W)-2)
        cv.circle(vis,(x,y),r,(0,255,0),2)
        cv.putText(vis,name,(x-r,y-r-4),cv.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1,cv.LINE_AA)
    cv.imwrite(path, vis)

# ---------- main ----------
def analyze_image(img):
    img = rectify(img)  # keep; comment out if your photos are already aligned
    rows_def = [("Row 1 (top)","upper_left","upper_right"),
                ("Row 2 (bottom)","lower_left","lower_right")]
    rows=[]
    for row_name,L,R in rows_def:
        A,Va = measure(img,L); B,Vb = measure(img,R)
        ratio, code = decide(A,Va,B,Vb)
        rows.append(PairResult(round(A,4),round(B,4),round(ratio,4),code,row_name))
    return {"rows":[asdict(x) for x in rows],
            "thresholds":{"RATIO_HI":RATIO_HI,"RATIO_LO":RATIO_LO,"V_BLACK":V_BLACK},
            "canvas":{"H":CANVAS[0],"W":CANVAS[1]}}, img

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chip_four_wells.py <image> [--debug out.png]"); sys.exit(1)
    im = read_image(sys.argv[1])
    result, rect = analyze_image(im)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if len(sys.argv) >= 4 and sys.argv[2] == "--debug":
        save_debug(rect, sys.argv[3])
