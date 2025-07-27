/**
 * PostCSS 配置檔案
 *
 * PostCSS 是一個用 JavaScript 轉換 CSS 的工具，透過插件系統來處理 CSS。
 * 此配置檔案定義了在構建過程中要使用的 PostCSS 插件。
 */
export const plugins = [
    /**
     * @tailwindcss/postcss - Tailwind CSS PostCSS 插件
     *
     * 這個插件負責處理 Tailwind CSS 框架的工具類別 (utility classes)。
     * 它會掃描專案中的 HTML、JavaScript 和其他檔案，找出使用的 Tailwind 類別，
     * 然後生成對應的 CSS 樣式，並移除未使用的樣式以優化檔案大小。
     */
    "@tailwindcss/postcss",

    /**
     * autoprefixer - CSS 自動前綴插件
     *
     * 這個插件會自動為 CSS 屬性添加瀏覽器前綴 (vendor prefixes)，
     * 例如 -webkit-、-moz-、-ms- 等，以確保 CSS 在不同瀏覽器中的相容性。
     * 它根據 browserslist 配置來決定需要支援的瀏覽器版本。
     */
    "autoprefixer",
];
