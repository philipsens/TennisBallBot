import React from 'react'
import * as classnames from "classnames";

const Button = ({ className, primary, secondary, accent, ...props }) => (
    <button
        className={classnames(className, 'button', {primary, secondary, accent})}
        {...props}
    />
)

export default Button