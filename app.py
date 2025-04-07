from flask import Flask, request, jsonify, send_file, render_template
import json
import tempfile
import os
import zipfile

app = Flask(__name__)


# Language extensions
def get_extension(language):
    return {"Java": "java", "C#": "cs", "Kotlin": "kt"}.get(language, "txt")


# Generate code based on language
def generate_code_for_language(class_name, content, language, case_style):
    if language == "Java":
        return generate_java_code(class_name, content, case_style)
    elif language == "C#":
        return generate_csharp_code(class_name, content, case_style)
    elif language == "Kotlin":
        return generate_kotlin_code(class_name, content, case_style)
    else:
        raise ValueError("Unsupported language")


# Convert snake_case or camelCase
def format_field(name, case_style):
    if case_style == "snake_case":
        return name.lower()
    else:  # camelCase
        return "".join(
            word.capitalize() if i else word for i, word in enumerate(name.split("_"))
        )


# Generate Java class
def generate_java_code(class_name, content, case_style):
    fields = ""
    getters_setters = ""

    for key, _ in content.items():
        field_name = format_field(key, case_style)
        fields += f"    private String {field_name};\n"

        # Getter
        getters_setters += f"""
    public String get{field_name.capitalize()}() {{
        return {field_name};
    }}

    public void set{field_name.capitalize()}(String {field_name}) {{
        this.{field_name} = {field_name};
    }}
"""
    return f"""
public class {class_name} {{
{fields}
{getters_setters}
}}
"""


# C# class
def generate_csharp_code(class_name, content, case_style):
    fields = ""
    for key, _ in content.items():
        field_name = format_field(key, case_style)
        fields += f"    public string {field_name.capitalize()} {{ get; set; }}\n"
    return f"""
public class {class_name} {{
{fields}
}}
"""


# Kotlin class
def generate_kotlin_code(class_name, content, case_style):
    fields = ", ".join(
        [f"val {format_field(key, case_style)}: String" for key in content.keys()]
    )
    return f"data class {class_name}({fields})"


@app.route("/")
def form():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_code():
    data = request.json
    json_input = data["json_data"]
    language = data["language"]
    case_style = data["case_style"]

    parsed_json = json.loads(json_input)

    files = {}

    # If multiple roots
    if isinstance(parsed_json, dict):
        for root_name, root_content in parsed_json.items():
            if isinstance(root_content, dict):
                code = generate_code_for_language(
                    root_name.capitalize(), root_content, language, case_style
                )
                files[f"{root_name.capitalize()}.{get_extension(language)}"] = code
            else:
                return jsonify({"error": "Each root must be an object"})
    else:
        return jsonify({"error": "Top-level JSON must be an object"})

    return jsonify(files)


@app.route("/download", methods=["POST"])
def download_code():
    files = request.json.get("files", {})

    with tempfile.TemporaryDirectory() as temp_dir:
        filenames = []

        for filename, code in files.items():
            file_path = os.path.join(temp_dir, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            filenames.append(file_path)

        zip_path = os.path.join(temp_dir, "dtos.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file in filenames:
                zipf.write(file, arcname=os.path.basename(file))

        return send_file(zip_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
