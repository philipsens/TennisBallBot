import React from 'react'
import * as classnames from "classnames";

const Zone = ({middle, corner, selected, collection, onZoneSelected, onCollectionSelected, disabled, all}) =>
    <div onClick={corner ? onCollectionSelected : (disabled ? null : onZoneSelected)}
         className={classnames('zone', {middle, selected, collection, disabled, corner})}/>

export default Zone