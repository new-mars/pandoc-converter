from flask import Flask, render_template, request, send_from_directory, send_file
import os
import subprocess
import shutil
import sys

# 添加 pandoc 到环境变量
os.environ['PATH'] = os.environ['PATH'] + r';C:\Program Files\Pandoc'

app = Flask(__name__)

# 设置上传文件夹和输出文件夹
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'docx', 'html'}

# 文件类型到 pandoc 输入格式的映射
FORMAT_MAPPING = {
    'docx': 'docx',
    'word': 'docx',
    'html': 'html'
}

# 确保必要的文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def check_pandoc():
    """检查 pandoc 是否可用"""
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, 
                              text=True,
                              shell=True)
        print("Pandoc 版本信息:", result.stdout)
        return True
    except Exception as e:
        print("Pandoc 检查错误:", str(e))
        return False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    """下载转换后的文件"""
    try:
        return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)
    except Exception as e:
        print(f"下载文件时出错: {str(e)}")
        return f"下载文件失败: {str(e)}", 404

@app.route('/convert', methods=['POST'])
def convert():
    try:
        print("\n=== 开始新的转换请求 ===")
        
        # 获取项目根目录的绝对路径
        base_dir = os.path.abspath(os.path.dirname(__file__))
        upload_dir = os.path.join(base_dir, UPLOAD_FOLDER)
        output_dir = os.path.join(base_dir, OUTPUT_FOLDER)
        
        print(f"基础目录: {base_dir}")
        print(f"上传目录: {upload_dir}")
        print(f"输出目录: {output_dir}")
        
        if not check_pandoc():
            print("Pandoc 检查失败")
            return 'Pandoc 未找到，请确保已正确安装', 500
            
        if 'files' not in request.files:
            print("请求中没有文件")
            return '没有选择文件', 400
        
        files = request.files.getlist('files')
        file_type = request.form.get('type')
        
        print(f"文件类型: {file_type}")
        print(f"接收到的文件数量: {len(files)}")
        print("文件名列表:", [f.filename for f in files])
        
        # 确保文件夹存在
        for folder in [upload_dir, output_dir]:
            if os.path.exists(folder):
                print(f"清空文件夹: {folder}")
                shutil.rmtree(folder)
            print(f"创建文件夹: {folder}")
            os.makedirs(folder)
        
        conversion_results = []
        for file in files:
            try:
                if not file:
                    print("文件对象为空")
                    continue
                    
                print(f"\n处理文件: {file.filename}")
                
                if not allowed_file(file.filename):
                    print(f"不支持的文件类型: {file.filename}")
                    continue
                    
                # 使用绝对路径
                input_path = os.path.join(upload_dir, file.filename)
                output_filename = os.path.splitext(file.filename)[0] + '.md'
                output_path = os.path.join(output_dir, output_filename)
                
                # 保存上传的文件
                file.save(input_path)
                print(f"文件已保存到: {input_path}")
                print(f"文件大小: {os.path.getsize(input_path)} 字节")
                
                try:
                    input_format = FORMAT_MAPPING.get(file_type)
                    if not input_format:
                        print(f"未知的文件类型: {file_type}")
                        conversion_results.append(f'不支持的文件类型: {file_type}')
                        continue
                    
                    # 构建命令
                    command = [
                        'pandoc',
                        '--from', input_format,
                        '--to', 'markdown',
                        input_path,
                        '--output', output_path,
                        '--wrap=none'
                    ]
                    
                    print(f"执行命令: {' '.join(command)}")
                    print(f"当前工作目录: {os.getcwd()}")
                    
                    # 执行转换
                    result = subprocess.run(
                        command,
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    
                    print("命令执行完成")
                    print("标准输出:", result.stdout)
                    print("标准错误:", result.stderr)
                    
                    # 检查输出文件
                    if os.path.exists(output_path):
                        print(f"输出文件存在: {output_path}")
                        with open(output_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if content.strip():
                                msg = f'文件 {file.filename} 转换成功 <a href="/download/{output_filename}">下载</a>'
                                print(f"文件 {file.filename} 转换成功")
                                conversion_results.append(msg)
                            else:
                                msg = f'文件 {file.filename} 转换失败：输出文件为空'
                                print(msg)
                                conversion_results.append(msg)
                    else:
                        msg = f'文件 {file.filename} 转换失败：输出文件未生成'
                        print(msg)
                        print(f"输出目录内容: {os.listdir(output_dir)}")
                        conversion_results.append(msg)
                
                except subprocess.CalledProcessError as e:
                    error_msg = f'转换文件 {file.filename} 时出错: {e.stderr}'
                    print(f"命令执行错误: {e}")
                    print(f"错误输出: {e.stderr}")
                    print(f"标准输出: {e.stdout}")
                    conversion_results.append(error_msg)
                    continue
                    
            except Exception as e:
                print(f"处理文件 {file.filename} 时发生错误: {str(e)}")
                conversion_results.append(f'处理文件 {file.filename} 时发生错误: {str(e)}')
                continue
        
        if not conversion_results:
            print("没有成功转换任何文件")
            return '没有可转换的文件', 400
        
        result = '<br>'.join(conversion_results) + '<br>文件已保存到 output 文件夹'
        print(f"返回结果: {result}")
        return result

    except Exception as e:
        print(f"处理请求时发生错误: {str(e)}")
        return f'服务器错误: {str(e)}', 500

    finally:
        print("=== 转换请求处理完成 ===\n")

if __name__ == '__main__':
    if not check_pandoc():
        print("警告：未找到 pandoc，请确保已正确安装并添加到系统 PATH 中")
    app.run(debug=True) 