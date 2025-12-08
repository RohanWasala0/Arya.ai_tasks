# 🚀 Arya.ai Document Processing Service  
A **FastAPI-based microservice** built during my internship at **Arya.ai**, providing two major capabilities:

1. **Background Removal** (powered by `rembg` + `u2net`)  
2. **Document Quality + Hologram + Signature Detection** (powered by Arya.ai’s internal APIs)


---

## 📌 Features

### ✅ 1. Background Removal API
- Removes background from images using the **Rembg** library.  
- Uses the **U2Net** deep learning model.  
- Supports high-resolution document and object images.  
- Runs heavy image processing tasks in a **threadpool** to avoid blocking the event loop.

---

### ✅ 2. Document Checker API
Uses Arya.ai's highly accurate document-analysis AI APIs:

#### 🔍 Quality Check  
- Sends the document to Arya.ai's API.  
- Rejects blurry/low-resolution or poor-lighting documents.  
- Only proceeds if the quality score passes the threshold.

#### ✨ Hologram Detection  
- Identifies whether the document contains holograms (tampering indicator).

#### ✒️ Signature Detection  
- Checks presence or absence of user signatures.
