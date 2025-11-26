import { CloseCircleFilled, CheckCircleFilled, } from '@ant-design/icons';
import { faBatteryEmpty, faBatteryFull, faBatteryHalf, faBatteryQuarter, faBatteryThreeQuarters, } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon, } from '@fortawesome/react-fontawesome';
import { useNavigation, } from '@refinedev/core';
import { Button, Table, Tag, Tooltip, Typography, } from 'antd';
import { formatDistanceToNow, intlFormat, } from 'date-fns';
import { useTranslation, } from 'react-i18next';

import type { Device, } from '../data/models';
import { capitaliseFirstLetter, } from '../utils/strings';
import { ResourceList, } from './ResourceList';

export const DeviceList = () => {
    const { show, } = useNavigation();

    const { t, } = useTranslation();

    return (
        <ResourceList<Device> resource='devices'>
            {() => (
                <>
                    <Table.Column<Device>
                        width={80}
                        dataIndex='lastSeen'
                        title={t('labels.device.status')}
                        align='center'
                        render={(value : string) => new Date().getTime() - new Date(value).getTime() > 24 * 60 * 60 * 1000 ? (
                            <CloseCircleFilled style={{
                                fontSize : 16,
                                color    : '#f44336',
                            }} />
                        ) : (
                            <CheckCircleFilled style={{
                                fontSize : 16,
                                color    : '#4caf50',
                            }} />
                        )} />
                    <Table.Column<Device>
                        dataIndex='displayName'
                        title={t('labels.device.displayName')}
                        render={(value, record) => {
                            const handleClick = () => show('devices', record.id);

                            return (
                                <Button
                                    size='small'
                                    type='link'
                                    onClick={handleClick}>
                                    {value ?? t('placeholders.notSet')}
                                </Button>
                            );
                        }} />
                    <Table.Column<Device>
                        width={120}
                        dataIndex='battery'
                        title={t('labels.device.battery')}
                        align='center'
                        render={(value : number) => {
                            let icon  = faBatteryEmpty;
                            let color = '#f44336';

                            if (value >= 75) {
                                icon  = faBatteryFull;
                                color = '#4caf50';
                            } else if (value >= 50) {
                                icon  = faBatteryThreeQuarters;
                                color = '#8bc34a';
                            } else if (value >= 25) {
                                icon  = faBatteryHalf;
                                color = '#ffeb3b';
                            } else if (value > 10) {
                                icon  = faBatteryQuarter;
                                color = '#ff9800';
                            }

                            return value > 0 ? (
                                <Tooltip title={`${value}%`}>
                                    <FontAwesomeIcon
                                        style={{
                                            color,
                                            fontSize : 16,
                                        }}
                                        icon={icon} />
                                </Tooltip>
                            ) : null;
                        }} />
                    <Table.Column<Device>
                        width={200}
                        dataIndex='mode'
                        title={t('labels.device.mode')}
                        render={(value : string) => (
                            <>
                                {value && value.includes('actuator') && (
                                    <Tag
                                        style={{
                                            marginRight : 8,
                                            cursor      : 'default',
                                        }}
                                        color='#7b1fa2'>
                                        {t('labels.device.modes.actuator')}
                                    </Tag>
                                )}
                                {value && value.includes('sensor') && (
                                    <Tag
                                        style={{
                                            cursor : 'default',
                                        }}
                                        color='#0097a7'>
                                        {t('labels.device.modes.sensor')}
                                    </Tag>
                                )}
                                {!value && (
                                    <Typography.Text>
                                        {t('placeholders.notSet')}
                                    </Typography.Text>
                                )}
                            </>
                        )} />
                    <Table.Column<Device>
                        width={200}
                        dataIndex='lastSeen'
                        title={t('labels.device.lastSeen')}
                        render={(value : string) => (
                            <Tooltip title={
                                intlFormat(value, {
                                    dateStyle : 'medium',
                                    timeStyle : 'medium',
                                }, {
                                    locale : navigator.language,
                                })}>
                                <Typography.Text style={{
                                    cursor : 'default',
                                }}>
                                    {capitaliseFirstLetter(formatDistanceToNow(new Date(value), {
                                        addSuffix : true,
                                    }))}
                                </Typography.Text>
                            </Tooltip>
                        )} />
                </>
            )}
        </ResourceList>
    );
};
