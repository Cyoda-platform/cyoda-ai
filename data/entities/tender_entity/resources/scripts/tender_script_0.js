var notices = [];
var Notice = Java.type('net.cyoda.saas.model.Notice');
// Add notices from input
for (var i = 0; i < input.notices.length; i++) {
    var notice = new Notice();
    notice.setId(input.notices[i].id != null ? input.notices[i].id : 0);
    notice.setDate(input.notices[i].date != null ? input.notices[i].date : "00-00-00");
    notice.setType(input.notices[i].type != null ? input.notices[i].type : "Unknown type");
    notices.push(notice);
}
entity.setNotices(notices);
