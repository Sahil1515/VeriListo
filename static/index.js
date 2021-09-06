// $(document).ready(function() {

//     jQuery.fn.single_double_click = function(single_click_callback, double_click_callback, timeout) {
//         return this.each(function() {
//             var clicks = 0,
//                 self = this;
//             jQuery(this).click(function(event) {
//                 clicks++;
//                 if (clicks == 1) {
//                     setTimeout(function() {
//                         if (clicks == 1) {
//                             single_click_callback.call(self, event);
//                         } else {
//                             double_click_callback.call(self, event);
//                         }
//                         clicks = 0;
//                     }, timeout || 300);
//                 }
//             });
//         });
//     }

//     $(".li_item").single_double_click(
//         function() {

//             var class_name = "unchecked";
//             var tag = $(this).html()

//             var class_get = $(this).attr('class');

//             if (class_get.includes('unchecked')) {
//                 class_name = "checked";
//             } else {
//                 class_name = "unchecked";
//             }

//             $.post("/updateClass_api", {
//                     "class_name": class_name,
//                     "tag": tag,
//                     "csrfmiddlewaretoken": "{{csrf_token}}"
//                 },
//                 function(data, status) {
//                     if (status == "success") {} else {
//                         alert("Failed!")
//                             // msg, couldnt be deleted
//                     }
//                 }

//             )


//             if (class_get.includes('unchecked') == true) {

//                 $(this).removeClass("unchecked");
//                 $(this).addClass("checked");

//             } else {
//                 $(this).removeClass("checked");
//                 $(this).addClass("unchecked");
//             }
//         },
//         function() {
//             var val_ele = $(this).html()

//             $(this).remove();


//             $.post("/delete_api", {
//                     "val": val_ele,
//                     "csrfmiddlewaretoken": "{{ csrf_token }}"
//                 },
//                 function(data, status) {
//                     if (status == "success") {
//                         // alert(data)
//                     } else {
//                         alert("Failed!")
//                     }
//                 }

//             )
//         })
// });









// // var str = "";

// // $('#add_btn').click(function() {

// //     var tag = $("#input").val();

// //     $.post("/", {
// //             "tag": tag,
// //             "csrfmiddlewaretoken": "{{csrf_token}}"
// //         },
// //         function(data, status) {
// //             if (status == "success") {
// //                 // flag = 1;

// //                 $("#input").val("");
// // alert("Hey")

// // var items = data['items'];
// // for (var i = 0; i < items.length; i++) {
// //     str +=
// //         '<div class="col-12 justify-content-center  align-content-center">' +
// //         '<li id="li_items" class="cross li_item ' + items[i]['class_name'] + '">' + items[i]['tag'] + "</li>"

// //     +
// //     '</div>'
// // }
// // var str = '<ul id="myUL" style="width: 100%;">' + str + '</ul>'

// // alert(str)
// // $('#myUL').html(str)




// // var str = '<li id="li_items" class="cross li_item ' + "unchecked" + '">' + tag + "</li>"
// // alert(str)
// // $('#myUL').append(str);


// //             } else {
// //                 alert("Failed!")
// //                     // msg, couldnt be deleted
// //             }
// //         }

// //     )
// // })