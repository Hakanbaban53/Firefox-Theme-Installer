# Adding a New Language

To add a new language to the Firefox Theme Installer, follow these steps:

1. **Create a Language File**
    - Navigate to the language data directory (`src/data/language`). [Link to the directory](../src/data/language)
    - Create a new JSON file with the language code as the filename (e.g., `fr.json` for French).
    - Make sure to create the file in every directory under `language` (e.g., `src/data/language`, `src/data/language/components`, `src/data/language/pages`, etc.).

    > Note: You need the reference of the version number on `language/app/<language_code>.json` file with `{version}` placeholder. For example, in `en.json`, you should add:
    ```json
    {
        "installer_version": "Theme Installer Version: V{version}"
    }
    ```

2. **Translate Strings**
    - Open the newly created language file.
    - Copy the content from `en.json` (English) and translate each string into the new language.
    - Make sure to keep the same structure and format as the original file.

3. **Update the Language List**
    - Open the `global_data.py` file in the `src/data/static` directory. [Link to the file](../src/data/static/global_data.py#L7)
    - Add the new language to the `LANGUAGES` list with the language code and name (e.g., `{"en": "English", "fr": "French"}`). For example:
    ```python
    LANGUAGES = [
        {"en": "English", "tr": "Türkçe", "fr": "French"},
    ]
    ```
    - If you wonder it will be your default language, app detects your system language and if it is in the list, it will be your default language. If not, it will be English. Also when you change the language, it will be saved in the `settings.json` file and it will be your default language when you open the app again. (If you want to reset the language, you can delete the `settings.json` file under the cache directory. [Here is the directories](../src/data/static/os_properties.py))

4. **Test the New Language**
    - Run the application.
    - Select the new language from the left dropdown button.
    - Verify that all strings are correctly translated and displayed.

5. **Submit Your Changes**
    - Commit your changes to the repository.
    - Create a pull request for review.

By following these steps, you can successfully add a new language to the Firefox Theme Installer. If you have any questions or need assistance, feel free to reach out to the project maintainers.
