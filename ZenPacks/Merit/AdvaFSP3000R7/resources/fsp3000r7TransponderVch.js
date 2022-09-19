(function(){

var ZC = Ext.ns('Zenoss.component');


function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.FSP3000R7TransponderVchPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'FSP3000R7TransponderVch',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'name'},
                {name: 'interfaceConfigId'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'inventoryUnitName'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true,
                width: 200
            },{
                id: 'interfaceConfigId',
                dataIndex: 'interfaceConfigId',
                header: _t('Comment'),
                sortable: true,
                width: 400
            },{
                id: 'inventoryUnitName',
                dataIndex: 'inventoryUnitName',
                header: _t('Model'),
                sortable: true,
                width: 150
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                sortable: true
            }]
        });
        ZC.FSP3000R7TransponderVchPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('FSP3000R7TransponderVchPanel', ZC.FSP3000R7TransponderVchPanel);
ZC.registerName('FSP3000R7TransponderVch', _t('Transponder Virtual Channel'), _t('Transponder Virtual Channels'));
})();


