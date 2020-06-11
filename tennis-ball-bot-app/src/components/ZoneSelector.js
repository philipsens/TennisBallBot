import React, {useState} from 'react'
import Zone from "./Zone";

export default function ZoneSelector({collectionMode}) {
    const [selectedCollection, setSelectedCollection] = useState(0);
    const [selectedZone, setSelectedZone] = useState(-1);
    const zones = [...new Array(12)].map((_, i) => ({
        middle: i === 4 || i === 7,
        corner: i === 0 || i === 2 || i === 9 || i === 11,
        disabled: collectionMode === 'disabled',
        all: collectionMode === 'all'
    }));

    return (
        <div className="zone-selector">
            {zones.map((zone, i) => (
                <Zone
                    key={i}
                    onZoneSelected={() => setSelectedZone(i)}
                    onCollectionSelected={() => setSelectedCollection(i)}
                    selected={i === selectedZone || collectionMode === 'all'}
                    collection={i === selectedCollection}
                    {...zone}
                />
            ))}
        </div>
    );
}
