import Image from "next/image";
import PinkCloudLogo from "../../../public/pinkcloud.png"; import VercelLogo from "../../../public/vercel.svg";

export default function Header({ className }: { className?: string }) {
  return (
    <header
      className={`flex items-center justify-center text-gray-200 text-2xl ${className}`}
    >
      <Image
        src={PinkCloudLogo}
        alt="pinkcloud-logo"
        width="160"
        height="50"

      />{" "}
      <div className="text-3xl ml-3 mr-3">/</div>

    </header>
  );
}