// app/layout.tsx
import { CartProvider } from "@/components/general/home-page/utils/cart-provider";
import "../styles/globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import { ThemeRegistry } from "@/components/theme-registry"; // You will create this

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning={true}>
      <body>
        {/* Wrap with registry to sync dynamic theme */}
        <ThemeRegistry>
          <ThemeProvider
            attribute="class"
            defaultTheme="light"
            enableSystem={false}
          >
            <CartProvider>{children}</CartProvider>
          </ThemeProvider>
        </ThemeRegistry>
      </body>
    </html>
  );
}
