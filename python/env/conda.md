# Clone new env
- 打开终端或命令提示符窗口，并激活当前要复制的源环境（如果尚未激活）。
- 运行以下命令，将源环境的所有依赖项导出到一个YAML文件中：
```bash
conda env export > environment.yml
```
- 使用文本编辑器打开导出的YAML文件（例如environment.yml），**并修改环境的名称为新环境的名称。确保修改了name字段，将其设置为新环境的名称**。
- 在终端或命令提示符窗口中，运行以下命令创建新的环境，并根据修改后的YAML文件进行配置：
```bash
conda env create -f environment.yml
```
完成后，新的环境将被创建并配置完成。
