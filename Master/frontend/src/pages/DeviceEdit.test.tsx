import { render, } from '../utils/test';
import { DeviceEdit, } from './DeviceEdit';

const mockGetFieldValue = vi.fn();

describe('<DeviceEdit />', () => {
    vi.mock('./ResourceEdit', () => ({
        ResourceEdit : ({
            children,
            ...props
        } : any) => (
            <form data-testid='resource-edit-form'>
                {children({
                    form : {
                        getFieldValue : mockGetFieldValue,
                    },
                    ...props,
                })}
            </form>
        ),
    }));

    it('renders displayName input', () => {
        const { getByLabelText, } = render(<DeviceEdit />);

        expect(getByLabelText('labels.device.displayName')).toBeInTheDocument();
    });

    it('renders mode select with options', () => {
        const { getByLabelText, } = render(<DeviceEdit />);

        expect(getByLabelText('labels.device.mode')).toBeInTheDocument();
    });

    it('normalizes mode select values correctly', () => {
        const normalize = DeviceEdit().props.children().props.children[1].props.normalize;

        expect(normalize([
            'sensor',
            '',
            'actuator',
        ])).toBe('sensor,actuator');

        expect(normalize('sensor')).toBe('sensor');
    });

    it('getValueProps splits comma-separated string', () => {
        const getValueProps = DeviceEdit().props.children().props.children[1].props.getValueProps;

        expect(getValueProps('sensor,actuator')).toEqual({
            value : [
                'sensor',
                'actuator',
            ],
        });

        expect(getValueProps([
            'sensor',
        ])).toEqual({
            value : [
                'sensor',
            ],
        });
    });

    it('renders with empty mode', () => {
        mockGetFieldValue.mockReturnValueOnce('');

        const { getByLabelText, } = render(<DeviceEdit />);

        expect(getByLabelText('labels.device.mode')).toBeInTheDocument();
    });

    it('renders children in ResourceEdit', () => {
        const { getByTestId, } = render(<DeviceEdit />);

        expect(getByTestId('resource-edit-form')).toBeInTheDocument();
    });

    it('handles multiple mode selection', () => {
        const { getByLabelText, } = render(<DeviceEdit />);

        expect(getByLabelText('labels.device.mode')).toBeInTheDocument();
    });

    it('handles undefined mode gracefully', () => {
        mockGetFieldValue.mockReturnValueOnce(undefined);

        const { getByLabelText, } = render(<DeviceEdit />);

        expect(getByLabelText('labels.device.mode')).toBeInTheDocument();
    });
});
