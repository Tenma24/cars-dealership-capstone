export default [{
  files: ["**/*.js", "**/*.jsx", "**/*.mjs"],
  languageOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
    parserOptions: { ecmaFeatures: { jsx: true } },
    globals: Object.fromEntries(["window", "document", "fetch", "FormData", "location", "history", "console", "process", "require", "module", "Buffer", "__dirname"].map(name => [name, "readonly"]))
  },
  rules: {
    "no-undef": "error", "no-unreachable": "error", "no-dupe-args": "error",
    "no-dupe-keys": "error", "no-duplicate-case": "error", "valid-typeof": "error"
  }
}];
