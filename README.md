# JSON to DTO Generator

This project is a web-based tool for generating Data Transfer Objects (DTOs) from JSON input. It supports multiple programming languages and case styles, making it easy to convert JSON data into structured code.

## Features

- **Supported Languages**: Java, Typescript, C#, Kotlin.
- **Case Styles**: `camelCase`,`snake_case`,`PascalCase`,`kebab-case`.
- **Preview**: View the generated DTOs directly in the browser.
- **Download**: Download the generated DTOs as a ZIP file.

## Project Structure

── app.py # Backend Flask application ├── templates/ │ └── index.html # Frontend HTML template ├── static/ │ └── styles.css # CSS styles for the frontend ├── sample.json # Example JSON input ├── requirements.txt # Python dependencies └── README.md # Project documentation

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Flask (`pip install flask`)

### Installation

1. Clone the repository:
   ```bash
   git clone <https://github.com/rrmytme/DTOGenerator-miniType.git>
   cd DTOGenerator-miniType
   ```

Usage
Upload a JSON file or paste JSON data.
Select the target programming language (Java, Typescript, C#, Kotlin).
Choose the desired case style (camelCase or snake_case or PascalCase or kebab-case).
Click "Generate DTOs" to preview the generated code.
Optionally, click "Download DTOs" to download the generated files as a ZIP.
Example
Input JSON
Output (Java)
Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

License
This project is licensed under the MIT License. See the LICENSE file for details.
