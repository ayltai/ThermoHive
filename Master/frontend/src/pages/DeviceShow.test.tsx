import { intlFormat, } from 'date-fns';

import { render, } from '../utils/test';
import { DeviceShow, } from './DeviceShow';

const mockData = {
    data : {
        id          : 1,
        displayName : 'Test Device',
        mode        : 'sensor,actuator',
        lastSeen    : new Date().toISOString(),
    },
};

vi.mock('./ResourceShow', () => ({
    ResourceShow : ({
        children,
    } : any) => (
        <div>
            {children({
                data : mockData,
            })}
        </div>
    ),
}));

describe('<DeviceShow />', () => {
    it('renders displayName input', () => {
        const { getByText, } = render(<DeviceShow />);

        expect(getByText('labels.device.displayName')).toBeInTheDocument();
    });

    it('renders mode tags for sensor and actuator', () => {
        const { getByText, } = render(<DeviceShow />);

        expect(getByText('labels.device.modes.sensor')).toBeInTheDocument();
        expect(getByText('labels.device.modes.actuator')).toBeInTheDocument();
    });

    it('renders lastSeen value', () => {
        const { getByText, } = render(<DeviceShow />);

        expect(getByText('labels.device.lastSeen')).toBeInTheDocument();
        expect(getByText(intlFormat(new Date(mockData.data.lastSeen), {
            dateStyle : 'medium',
            timeStyle : 'medium',
        }, {
            locale : navigator.language,
        }))).toBeInTheDocument();
    });
});
