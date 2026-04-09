import { Canvas, useLoader } from "@react-three/fiber";
import { Sphere, OrbitControls } from "@react-three/drei";
import * as THREE from "three";

function Moon() {
  const texture = useLoader(THREE.TextureLoader, "/textures/moon.jpg");

  return (
    <Sphere args={[2, 64, 64]}>
      <meshStandardMaterial map={texture} />
    </Sphere>
  );
}

export default function MoonBackground() {
  return (
    <div className="absolute inset-0 -z-10 opacity-40">
      <Canvas>
        <ambientLight intensity={0.4} />
        <directionalLight position={[2, 2, 2]} intensity={1} />

        <Moon />

        <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.3} />
      </Canvas>
    </div>
  );
}
