import React, { useEffect, useState } from 'react';
import { HubConnectionBuilder } from '@microsoft/signalr';

interface LineupVisuals {
  id: string;
  targetZone: string;
  positionImgUrl: string;
  crosshairImgUrl: string;
  landingImgUrl: string;
}

export const ThreePictureParadigm: React.FC = () => {
  const [lineup, setLineup] = useState<LineupVisuals | null>(null);

  useEffect(() => {
    // Construct pipeline link to the active .NET central hub
    const connection = new HubConnectionBuilder()
      .withUrl("http://localhost:5000/lineuphub")
      .withAutomaticReconnect()
      .build();

    connection.on("ReceiveActiveLineups", (data: LineupVisuals[]) => {
      if (data && data.length > 0) {
        setLineup(data[0]); // Snaps to the single closest calculated tactical lineup match
      }
    });

    connection.start().catch(err => console.error("SignalR Connection Failure: ", err));
    return () => { connection.off("ReceiveActiveLineups"); };
  }, []);

  if (!lineup) return <div className="placeholder">Awaiting Map Positioning Telemetry...</div>;

  return (
    <div className="three-picture-panel">
      <h2>Active Target: <span className="highlight">{lineup.targetZone}</span></h2>
      <div className="image-grid">
        <div className="card"><h3>1. Stand Position</h3><img src={lineup.positionImgUrl} alt="Stand Position" /></div>
        <div className="card"><h3>2. Pixel Alignment</h3><img src={lineup.crosshairImgUrl} alt="Crosshair Alignment" /></div>
        <div className="card"><h3>3. Impact Landing</h3><img src={lineup.landingImgUrl} alt="Expected Output Result" /></div>
      </div>
    </div>
  );
};
