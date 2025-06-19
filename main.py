from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from PIL import Image
from rembg import remove
import io

app = FastAPI()

@app.post("/gerar-chibi")
async def gerar_chibi(file: UploadFile = File(...)):
    input_img = Image.open(file.file).convert("RGBA")
    img_no_bg = remove(input_img)

    gray_img = img_no_bg.convert("L")
    bw_img = gray_img.point(lambda x: 0 if x < 200 else 255, '1')
    final_bw = bw_img.convert("RGBA")

    width, height = input_img.size
    if height < width * 1.2:
        try:
            base_body = Image.open("chibi_coloring_page_clean.png").convert("RGBA")
            base_body = base_body.resize((800, 800))
            head_resized = final_bw.resize((300, 300))
            combined = base_body.copy()
            combined.paste(head_resized, (250, 80), head_resized)
            final_bw = combined
        except:
            pass

    output_path = "chibi_pb_result.png"
    final_bw.save(output_path, format="PNG")

    return FileResponse(output_path, media_type="image/png", filename="chibi_pb.png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
