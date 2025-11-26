import { faMicrochip, faTemperatureFull, } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon, } from '@fortawesome/react-fontawesome';

import { DeviceEdit, DeviceList, DeviceShow, TelemetryList, } from '../pages';

export const resources = [
    {
        name : 'devices',
        meta : {
            icon  : <FontAwesomeIcon icon={faMicrochip} />,
            label : 'resources.devices',
        },
        list : '/devices',
        edit : '/devices/edit/:id',
        show : '/devices/show/:id',
    }, {
        name : 'telemetry',
        meta : {
            icon  : <FontAwesomeIcon icon={faTemperatureFull} />,
            label : 'resources.telemetry',
        },
        list : '/telemetry',
    },
];

export const routes = [
    {
        path     : 'devices',
        children : [
            {
                index     : true,
                Component : DeviceList,
            }, {
                path      : 'edit/:id',
                Component : DeviceEdit,
            }, {
                path      : 'show/:id',
                Component : DeviceShow,
            },
        ],
    }, {
        path     : 'telemetry',
        children : [
            {
                index     : true,
                Component : TelemetryList,
            },
        ],
    },
];
