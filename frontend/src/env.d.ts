/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_USERNAME: string;
  readonly VITE_API_PASSWORD: string;
  readonly VITE_CWA_API_KEY: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
