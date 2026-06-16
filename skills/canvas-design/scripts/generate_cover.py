import sys
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

PROJECT_ID = "wechat-486216"
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

def generate_image_correctly(prompt_text):
    print(f"正在使用 Imagen 3 生成: {prompt_text} ...")

    try:
        model = ImageGenerationModel.from_pretrained("imagen-4.0-ultra-generate-001")
        images = model.generate_images(
            prompt=prompt_text,
            number_of_images=1,
            language="en",
            aspect_ratio="16:9",
            safety_filter_level="block_some",
            person_generation="allow_adult"
        )

        if images:
            output_filename = "imagen_output.png"
            images[0].save(location=output_filename, include_generation_parameters=False)
            print(f"成功生成图片并保存为: {output_filename}")
        else:
            print("未生成图片。")

    except Exception as e:
        print(f"生成失败: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:]).strip()
    else:
        prompt = "A futuristic banana character writing code on a laptop, cyberpunk style, neon lights, 4k resolution, high detail"
    if not prompt:
        print("用法: python scripts/generate_cover.py <微信公众号内容或英文 prompt>")
        sys.exit(1)
    generate_image_correctly(prompt)
