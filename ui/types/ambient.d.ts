/// <reference types="node" />
// Ambient module declarations for template Vite plugins used in `ui/templates`
// Prevents TypeScript "Cannot find module" errors when the template files
// are opened in the editor but the packages are not installed in this workspace.

declare module "@tanstack/devtools-vite"
declare module "@tanstack/react-start/plugin/vite"
declare module "vite-tsconfig-paths"

declare module "@vitejs/plugin-react" {
  import type { Plugin } from "vite"
  const plugin: (...args: any[]) => Plugin
  export default plugin
}

declare module "@tailwindcss/vite" {
  import type { Plugin } from "vite"
  const plugin: (...args: any[]) => Plugin
  export default plugin
}

declare module "nitro/vite" {
  import type { Plugin } from "vite"
  const nitro: (...args: any[]) => Plugin
  export { nitro }
  export default nitro
}
