/**
A container of AlerMessages. This container is perfect for top-of-form
messages. It defaults to beeing hidden. When you add a message it
becomes invisible, and when you remove all messages, it hides itself
automatically.
*/ 
Ext.define('devilry_extjsextras.AlertMessageList', {
    extend: 'Ext.panel.Panel',
    requires: [
        'devilry_extjsextras.AlertMessage'
    ],
    ui: 'transparentpanel',
    alias: 'widget.alertmessagelist',
    cls: 'devilry_extjsextras_alertmessagelist',
    hidden: true,

    initComponent: function() {
        this.on('remove', this._onRemove, this);
        this.callParent(arguments);
        this.addListener({
            scope: this,
            closed: this._onClose
        });
    },

    _onClose: function(alertmessage) {
        this.remove(alertmessage, true);
    },

    /** Create and add a ``devilry_extjsextras.AlertMessage``. The config parameter is
     * forwarded to the AlertMessage constructor. */
    add: function(config) {
        var message = Ext.widget('alertmessage', config);
        this.callParent([message]);
        message.enableBubble('closed');
        this.show();
    },
    
    _onRemove: function() {
        var messages = this.query('alertmessage');
        if(messages.length === 0) {
            this.hide();
        }
    },

    /** Add many messages of the same type.
     *
     * @param messages Array of messages (strings).
     * @param type The type of the message (see ``devilry_extjsextras.AlertMessage.type``).
     * */
    addMany: function(messages, type, closable) {
        Ext.Array.each(messages, function(message) {
            this.add({
                message: message,
                type: type,
                closable: closable
            });
        }, this);
    }
});
