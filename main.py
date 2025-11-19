from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Inquiry

app = FastAPI(title="War Marco API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health & DB test
@app.get("/test")
def test():
    try:
        # simple ping by listing collections (no error if db configured)
        _ = db.list_collection_names() if db else None
        return {"status": "ok", "database": bool(db)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Static product categories for now (images served from frontend public folder)
class ProductCategory(BaseModel):
    slug: str
    title: str
    description: str
    image: str
    specs: Optional[List[str]] = None

CATEGORIES: List[ProductCategory] = [
    ProductCategory(
        slug="rank-badges",
        title="Rank Badges",
        description="Embroidered and metal rank insignia manufactured to international military standards.",
        image="/images/rank-badges.jpg",
        specs=["Embroidery / Metal", "Custom sizes", "Colorfast threads", "Nickel / Brass / Antique finishes"],
    ),
    ProductCategory(
        slug="uniform-medals",
        title="Uniform Medals",
        description="Die-struck medals, ribbons, and mounting bars for service recognition.",
        image="/images/uniform-medals.jpg",
        specs=["Die-struck brass / zinc", "Enamel options", "Ribbon mounting", "Custom molds"],
    ),
    ProductCategory(
        slug="metal-buttons",
        title="Metal Buttons",
        description="High-polish and antique-finish metal buttons with custom crests.",
        image="/images/metal-buttons.jpg",
        specs=["Brass / Zinc", "Electroplated finishes", "Shank / Flat-back", "Custom die tooling"],
    ),
    ProductCategory(
        slug="p-caps",
        title="P-Caps",
        description="Headwear manufactured with premium fabrics and stitching for durability.",
        image="/images/p-caps.jpg",
        specs=["Wool / Cotton / Blends", "Custom embroidery", "Adjustable sizes", "Moisture-wicking"],
    ),
    ProductCategory(
        slug="p-cap-badges",
        title="P-Cap Badges",
        description="Metal and embroidered cap badges with secure fittings.",
        image="/images/p-cap-badges.jpg",
        specs=["Pin / Screw backings", "Nickel / Gold / Antique", "Custom crests", "Precision detailing"],
    ),
    ProductCategory(
        slug="shoulders-epaulettes",
        title="Shoulders & Epaulettes",
        description="Tailored epaulettes and shoulder boards for military and police uniforms.",
        image="/images/epaulettes.jpg",
        specs=["Velcro / Button closures", "Custom piping", "Gold braid options", "Pair matched"],
    ),
    ProductCategory(
        slug="ribbons",
        title="Ribbons",
        description="Service ribbons and bars with fade-resistant dyes and precise colors.",
        image="/images/ribbons.jpg",
        specs=["Colorfast", "All widths", "Mounting bars", "Bulk supply"],
    ),
    ProductCategory(
        slug="beret-badges",
        title="Beret Badges",
        description="High-detail metal beret badges with secure fittings and premium finishes.",
        image="/images/beret-badges.jpg",
        specs=["Die-struck", "Enamel fill", "Gold/Nickel/Antique", "Custom tooling"],
    ),
    ProductCategory(
        slug="custom-metal-accessories",
        title="Custom Metal Accessories",
        description="Custom metal insignia, crests, and accessories built to your specifications.",
        image="/images/custom-metal.jpg",
        specs=["OEM/ODM", "Rapid prototyping", "Finish library", "Strict QA"],
    ),
    ProductCategory(
        slug="all-uniform-accessories",
        title="All Uniform Accessories",
        description="Complete range for armed forces, police, and security uniforms.",
        image="/images/all-accessories.jpg",
        specs=["End-to-end supply", "Private label", "Global shipping", "Compliance docs"],
    ),
]

@app.get("/products", response_model=List[ProductCategory])
def list_products():
    return CATEGORIES

# Inquiry submission endpoint
@app.post("/inquiries")
def submit_inquiry(payload: Inquiry):
    try:
        doc_id = create_document("inquiry", payload)
        return {"success": True, "id": doc_id}
    except Exception as e:
        # Even if DB is not configured, return 200 with note to avoid blocking lead capture
        return {"success": False, "error": str(e)}
