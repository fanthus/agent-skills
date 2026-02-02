import os
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# 1. 配置
PROJECT_ID = "wechat-486216"
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

def generate_image_correctly(prompt_text):
    print(f"正在使用 Imagen 3 生成: {prompt_text} ...")
    
    try:
        # 2. 加载专门的生图模型 (Imagen 3)
        # 注意：这里使用的是 'imagen-3.0-generate-001'
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

        # 3. 生成图片
        images = model.generate_images(
            prompt=prompt_text,
            # 可选参数
            number_of_images=1,
            language="en",
            aspect_ratio="16:9", # 比如 "1:1", "16:9", "9:16"
            safety_filter_level="block_some",
            person_generation="allow_adult"
        )

        # 4. 保存结果
        if images:
            output_filename = "imagen_output.png"
            # images[0] 是生成的图片对象
            images[0].save(location=output_filename, include_generation_parameters=False)
            print(f"成功生成图片并保存为: {output_filename}")
            
            # 如果在 Jupyter/Colab 中，可以直接 images[0].show()
        else:
            print("未生成图片。")

    except Exception as e:
        print(f"生成失败: {e}")

if __name__ == "__main__":
    # 提示词建议使用英文以获得最佳效果
    prompt = "A futuristic banana character writing code on a laptop, cyberpunk style, neon lights, 4k resolution, high detail"
    generate_image_correctly(prompt)