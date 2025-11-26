import { render, } from '../utils/test';
import { DeviceEdit, } from './DeviceEdit';

const mockGetFieldValue = vi.fn();

describe('<DeviceEdit />', () => {
    vi.mock('./ResourceEdit', () => ({
        ResourceEdit : ({
            children,
        } : any) => (
            <form>
                {children({
                    form : {
                        getFieldValue : mockGetFieldValue,
                    },
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
});
