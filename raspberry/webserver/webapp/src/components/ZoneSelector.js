import React, {useEffect, useState} from 'react'
import Zone from "./Zone";
import {CollectionMode} from "../CollectionMode";
import {Zones} from "../Zones";

const baseURI = process.env.REACT_APP_API_URL;
const collectionURI = baseURI + 'collection';
const zoneURI = baseURI + 'zone';

export default function ZoneSelector({collectionMode}) {
    const [selectedCollection, setSelectedCollection] = useState(Zones.UpperLeftCorner);
    const [selectedZone, setSelectedZone] = useState(Zones.TopZone);
    const zones = [...new Array(12)].map((_, zoneID) => ({
        middle: zoneID === Zones.UpperMiddleZone
            || zoneID === Zones.LowerMiddleZone,
        corner: zoneID === Zones.UpperLeftCorner
            || zoneID === Zones.UpperRightCorner
            || zoneID === Zones.LowerLeftCorner
            || zoneID === Zones.LowerRightCorner,
        disabled: collectionMode === CollectionMode.DISABLED
    }));

    useEffect(() => {
        fetch(collectionURI)
            .then(response => response.json())
            .then(data => setSelectedCollection(data))

        fetch(zoneURI)
            .then(response => response.json())
            .then(data => setSelectedZone(data))
    }, [])

    useEffect(() => {
        fetch(collectionURI, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({collection: selectedCollection})
        })
            .catch(error => console.log(error))
    }, [selectedCollection])

    useEffect(() => {
        fetch(zoneURI, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({zone: selectedZone})
        })
            .catch(error => console.log(error))
    }, [selectedZone])

    return (
        <div className="zone-selector">
            {zones.map((zone, zoneID) => (
                <Zone
                    key={zoneID}
                    onCollectionSelected={() => setSelectedCollection(zoneID)}
                    onZoneSelected={() => setSelectedZone(zoneID)}
                    selected={zoneID === selectedZone || collectionMode === CollectionMode.ALL}
                    collection={zoneID === selectedCollection}
                    {...zone}
                />
            ))}
        </div>
    );
}
