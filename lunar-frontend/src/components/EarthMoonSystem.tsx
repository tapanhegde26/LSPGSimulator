/**
 * 3D Earth-Moon System Visualization
 * Interactive Three.js scene showing Earth, Moon, and energy transmission
 */
import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { 
  OrbitControls, 
  Stars, 
  Sphere, 
  Line,
  Html,
} from "@react-three/drei";
import * as THREE from "three";
import type { SimulationResponse } from "../types";

interface EarthMoonSystemProps {
  simulationData?: SimulationResponse | null;
  isStreaming?: boolean;
}

function Earth({ position }: { position: [number, number, number] }) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.1;
    }
  });

  return (
    <group position={position}>
      <Sphere ref={meshRef} args={[1, 64, 64]}>
        <meshStandardMaterial
          color="#1e40af"
          roughness={0.8}
          metalness={0.2}
        />
      </Sphere>
      {/* Atmosphere glow */}
      <Sphere args={[1.05, 32, 32]}>
        <meshBasicMaterial
          color="#60a5fa"
          transparent
          opacity={0.15}
          side={THREE.BackSide}
        />
      </Sphere>
      {/* Continents hint */}
      <Sphere args={[1.01, 32, 32]}>
        <meshStandardMaterial
          color="#22c55e"
          roughness={1}
          transparent
          opacity={0.3}
        />
      </Sphere>
    </group>
  );
}

function Moon({ position }: { position: [number, number, number] }) {
  const meshRef = useRef<THREE.Mesh>(null);
  const ringRef = useRef<THREE.Mesh>(null);
  
  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.05;
    }
    if (ringRef.current) {
      ringRef.current.rotation.z += delta * 0.02;
    }
  });

  return (
    <group position={position}>
      {/* Moon body */}
      <Sphere ref={meshRef} args={[0.27, 32, 32]}>
        <meshStandardMaterial
          color="#9ca3af"
          roughness={1}
          metalness={0}
        />
      </Sphere>
      
      {/* Solar Ring */}
      <mesh ref={ringRef} rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[0.35, 0.02, 16, 100]} />
        <meshStandardMaterial
          color="#3b82f6"
          emissive="#3b82f6"
          emissiveIntensity={0.5}
        />
      </mesh>
      
      {/* Ring glow */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[0.35, 0.05, 8, 50]} />
        <meshBasicMaterial
          color="#60a5fa"
          transparent
          opacity={0.2}
        />
      </mesh>
    </group>
  );
}

function EnergyBeam3D({ 
  start, 
  end, 
  intensity = 1 
}: { 
  start: [number, number, number]; 
  end: [number, number, number];
  intensity?: number;
}) {
  const points = useMemo(() => [
    new THREE.Vector3(...start),
    new THREE.Vector3(...end),
  ], [start, end]);

  return (
    <group>
      {/* Main beam */}
      <Line
        points={points}
        color="#22d3ee"
        lineWidth={2 * intensity}
        transparent
        opacity={0.5}
      />
      
      {/* Beam particles */}
      {[...Array(5)].map((_, i) => (
        <BeamParticle 
          key={i} 
          start={start} 
          end={end} 
          delay={i * 0.2}
          intensity={intensity}
        />
      ))}
    </group>
  );
}

function BeamParticle({ 
  start, 
  end, 
  delay,
  intensity,
}: { 
  start: [number, number, number]; 
  end: [number, number, number];
  delay: number;
  intensity: number;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current) {
      const t = ((state.clock.elapsedTime + delay) % 2) / 2;
      meshRef.current.position.x = start[0] + (end[0] - start[0]) * t;
      meshRef.current.position.y = start[1] + (end[1] - start[1]) * t;
      meshRef.current.position.z = start[2] + (end[2] - start[2]) * t;
      
      // Fade in/out
      const material = meshRef.current.material as THREE.MeshBasicMaterial;
      material.opacity = Math.sin(t * Math.PI) * 0.8;
    }
  });

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[0.03 * intensity, 8, 8]} />
      <meshBasicMaterial
        color="#22d3ee"
        transparent
        opacity={0.5}
      />
    </mesh>
  );
}

function GroundStations({ 
  stations,
  earthPosition,
}: { 
  stations?: Array<{ station_id: number; latitude?: number; longitude?: number }>;
  earthPosition: [number, number, number];
}) {
  if (!stations || stations.length === 0) return null;

  return (
    <group>
      {stations.slice(0, 10).map((station, i) => {
        // Convert lat/lon to 3D position on Earth surface
        const lat = station.latitude || (Math.random() * 120 - 60);
        const lon = station.longitude || (i * 36);
        
        const phi = (90 - lat) * (Math.PI / 180);
        const theta = (lon + 180) * (Math.PI / 180);
        
        const x = earthPosition[0] - 1.05 * Math.sin(phi) * Math.cos(theta);
        const y = earthPosition[1] + 1.05 * Math.cos(phi);
        const z = earthPosition[2] + 1.05 * Math.sin(phi) * Math.sin(theta);

        return (
          <mesh key={station.station_id} position={[x, y, z]}>
            <sphereGeometry args={[0.03, 8, 8]} />
            <meshBasicMaterial color="#f59e0b" />
          </mesh>
        );
      })}
    </group>
  );
}

function Scene({ simulationData, isStreaming }: EarthMoonSystemProps) {
  const earthPosition: [number, number, number] = [0, 0, 0];
  const moonPosition: [number, number, number] = [5, 0.5, 0];
  
  const beamIntensity = simulationData 
    ? Math.min(2, simulationData.system_efficiency * 2 + 0.5)
    : 1;

  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.2} />
      <directionalLight position={[10, 5, 5]} intensity={1} />
      <pointLight position={[-10, -5, -5]} intensity={0.3} color="#fef3c7" />
      
      {/* Stars background */}
      <Stars 
        radius={100} 
        depth={50} 
        count={5000} 
        factor={4} 
        saturation={0} 
        fade 
      />
      
      {/* Earth */}
      <Earth position={earthPosition} />
      
      {/* Moon with Solar Ring */}
      <Moon position={moonPosition} />
      
      {/* Energy Beam */}
      {(isStreaming || simulationData) && (
        <EnergyBeam3D 
          start={moonPosition} 
          end={earthPosition}
          intensity={beamIntensity}
        />
      )}
      
      {/* Ground Stations */}
      <GroundStations 
        stations={simulationData?.stations}
        earthPosition={earthPosition}
      />
      
      {/* Labels */}
      <Html position={[earthPosition[0], earthPosition[1] - 1.5, earthPosition[2]]}>
        <div className="text-blue-400 text-xs font-semibold whitespace-nowrap">
          Earth
        </div>
      </Html>
      <Html position={[moonPosition[0], moonPosition[1] - 0.6, moonPosition[2]]}>
        <div className="text-gray-400 text-xs font-semibold whitespace-nowrap">
          Moon
        </div>
      </Html>
      
      {/* Camera controls */}
      <OrbitControls 
        enablePan={false}
        minDistance={3}
        maxDistance={15}
        autoRotate={!isStreaming}
        autoRotateSpeed={0.5}
      />
    </>
  );
}

export default function EarthMoonSystem({ simulationData, isStreaming }: EarthMoonSystemProps) {
  return (
    <div className="w-full h-[400px] rounded-xl overflow-hidden bg-black/50">
      <Canvas
        camera={{ position: [0, 2, 8], fov: 45 }}
        gl={{ antialias: true }}
      >
        <Scene simulationData={simulationData} isStreaming={isStreaming} />
      </Canvas>
      
      {/* Overlay info */}
      <div className="absolute bottom-2 left-2 text-xs text-gray-500">
        Drag to rotate | Scroll to zoom
      </div>
      
      {simulationData && (
        <div className="absolute top-2 right-2 bg-black/50 rounded px-2 py-1 text-xs">
          <span className="text-green-400">
            {simulationData.total_energy_generated_gw.toFixed(0)} GW
          </span>
          <span className="text-gray-500 mx-1">→</span>
          <span className="text-blue-400">
            {simulationData.energy_received_gw.toFixed(0)} GW
          </span>
        </div>
      )}
    </div>
  );
}
