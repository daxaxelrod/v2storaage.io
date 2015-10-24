//
//
// FUCK JAVASCIPT FOR TODAY
//
// // jinja 2 variable can be used in js
// // for each div with class container-marketplace . seton click listener({{url_for('/marketplace/<post_id>', post_id=post_id)}})
//
// $('.container-marketplace').each(function(i,container){
// $(container).one("click",function(){
//
//
// //match variable names from with
//   $.getJSON($SCRIPT_ROOT + '/_render_single_listing', {a: container.id}, function(data) {
//         //select where to put the data
//         console.log(data);
//         //{{render_template('single_listing_template.html', listing = data)}} May work instead
//         // var num = data.listing_to_be_passed.toString();
//         // console.log(num);
//         // var array_of_nums = (""+num).split("").map(function(t){return parseInt(t)});
//         // var num_i_want = array_of_nums[10];
//         // console.log(num_i_want);
//         //
//         //NEED TO MAKE THE JUMP FROM JS TO JINJA
//
//
//
//
//         //window.location.href =
//                           //  ????    //{{render_template('single_listing_template.html', listing = )}}
//
//         });
//     // dont need to stop it cause its not a link
//     // return false;  stops it from doing default link behaviour
//     // so far cant use js variable in jinja but not entirely sure. TO GOOGle
//     //{{render_template('single_listing_template.html', listing=num_i_want)}}
//
//
//
//
//
//
//
//
// //maybe ajax is the right choice here
// // $.ajax({
// //   type:"POST",
// //   method: "POST",
// //   statusCode: {
// //     404: function(){
// //       alert("BRooo you messed up big time. PAGE NOT FOUND");
// //     }
// //   }
// //   url: "single_listing_template.html",
// //   success: function(data) {
// //     data = single_listing_yes_yes_yes;
// //     console.log(data);
// //     console.log("\n {{render_template(url_for(single_listing_yes_yes_yes), listing = data)}})"
// //
// //
// //
// //
// //
// //   }
// //
// //
// //
// });
//   // $.ajax({
//   //   type: "POST",
//   //   url: "notsure yet, can probally use the passed in objects though?",
//   //   success: function(data){
//   //     //this feels wrong. like bad uncle wrong
//   //
//   //   }
//   //
//   // }
//
//
//
// //  );
//
//   });
//
//     //ok this hrefs it
//     // now post container id
//     //awesome now posts have an id
//
//
//
//
//
//   // selects each of the divs. lets add an onclick listener
//     // container.click(function(){
//     //   console.log("Yo did this work? should be 5 or 6 times");
//     //
//     //
//     // });
//
//
//
// // console.log("YOLO SWAG");
// // console.log(i);
// // console.log(container);
// //MOTHERFUCKER HAD TO RESELECT??@??@?!!?! THE FUCK????
//
//   //console.log("YOOOO IT WORRDDDKKKKKSSSSS");
//   //lols enough play
//
//   // ok so i need the listing id of the container but i have
//   // 0 idea how to get it
//   //{{render_template(url_for("indi_listing", listing_id = listing_list[i]))}}
//
//   // these gotta be a way to post in js to a python file
//   // must send you to another page
//
//
//   //AJAX FOR THE WIN ???? LOSS BRooo
