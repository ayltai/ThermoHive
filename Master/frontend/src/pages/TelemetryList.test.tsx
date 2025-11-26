import { render, } from '../utils/test';
import { TelemetryList, } from './TelemetryList';

vi.mock('@refinedev/core', async () => ({
    ...(await vi.importActual('@refinedev/core')),
    useList       : () => ({
        result : {
            data : [
                {
                    id          : 'dev-1',
                    displayName : 'Device 1',
                },
                {
                    id          : 'dev-2',
                    displayName : 'Device 2',
                },
            ],
        },
    }),
    useNavigation : () => ({
        show : vi.fn(),
    }),
}));


vi.mock('./ResourceList', () => ({
    ResourceList : ({
        children,
    } : any) => (
        <div>
            {children({
                isLoading : false,
                isSuccess : true,
                sorters   : [],
                data      : {
                    data : [
                        {
                            id         : 1,
                            deviceId   : 'dev-1',
                            timestamp  : '2024-01-01T00:00:00Z',
                            sensorType : 'temperature',
                            value      : 42,
                        },
                    ],
                },
            })}
        </div>
    ),
}));

vi.mock('antd', async () => ({
    ...(await vi.importActual('antd')),
    Table      : {
        Column: ({
            title,
        } : any) => (
            <div>
                <span>{title}</span>
            </div>
        ),
    },
    Tag        : ({
        children,
    } : any) => (
        <span>
            {children}
        </span>
    ),
    Typography : {
        Text : ({
            children,
        } : any) => <span>{children}</span>,
    },
}));

describe('<TelemetryList />', () => {
    it('renders deviceId column', () => {
        const { getByText, } = render(<TelemetryList />);

        expect(getByText('labels.telemetry.deviceId')).toBeInTheDocument();
    });

    it('renders timestamp column', () => {
        const { getByText, } = render(<TelemetryList />);

        expect(getByText('labels.telemetry.timestamp')).toBeInTheDocument();
    });

    it('renders sensorType column', () => {
        const { getByText, } = render(<TelemetryList />);

        expect(getByText('labels.telemetry.sensorType')).toBeInTheDocument();
    });

    it('renders value column', () => {
        const { getByText, } = render(<TelemetryList />);

        expect(getByText('labels.telemetry.value')).toBeInTheDocument();
    });
});
