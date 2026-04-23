
import Navbar from "@/Components/Navbar";
import "./globals.css";


export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Navbar></Navbar>
        {children}
        <div className="footer" style={{width:"100vw", height:"10rem"}}></div>
      </body>
    </html>
  );
}
