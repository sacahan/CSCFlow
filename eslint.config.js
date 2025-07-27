const globals = require("globals");
const pluginReact = require("eslint-plugin-react");
const { defineConfig } = require("eslint/config");

module.exports = defineConfig([
    {
        files: ["**/*.{js,mjs,cjs,jsx}"],
        languageOptions: { globals: globals.browser },
    },
    pluginReact.configs.flat.recommended,
]);
