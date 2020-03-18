const openModalButtons = document.querySelectorAll('[data-modal-target]')
const closeModalButtons = document.querySelectorAll('[data-close-button]')
const overlay = document.getElementById('overlay')

openModalButtons.forEach(button => {
	button.addEventListener('click', () => {
		const modal = document.querySelector(button.dataset.modalTarget)
		openModal(modal)
	})
})

closeModalButtons.forEach(button => {
	button.addEventListener('click', () => {
		const modal = button.closest('.modal')
		closeModal(modal)
	})
})

function openModal(modal) {
	if (modal == null) return;
	modal.classList.add('active')
	overlay.classList.add('active')
}

function closeModal(modal) {
	if (modal == null) return;
	modal.classList.remove('active')
	overlay.classList.remove('active')
}

/*________________________________________________________________________________________________*/

const areas = document.querySelectorAll(".area")

areas.forEach(area => {
	area.addEventListener('click', () => {
		create_table(zone_code = area.title, zone_name = area.attributes["name"].value)
	})
})

/*________________________________________________________________________________________________*/

for (var i=0, len = all_diseases.length; i<len; i++) {
  all_diseases[i].onclick = updateDict;
}

function updateDict(e) {
  if (this.checked) {
    choices[this.value] = this.value;
  } else {
     if (choices.hasOwnProperty(this.value)) {
        delete choices[this.value];
     }
  }
}


function create_table(zone_code, zone_name) {
	current_dist = zone_code;
	var info = json_dict_full[zone_code];
	total_rows = info[0].length + 1;
	total_columns = info[1].length + 1;
	var choices_indexes = [];

	for (choice in choices) {
		temp = info[1].findIndex(element => element == choice);
		if (temp > -1) choices_indexes.push(temp);
	}


	var mytable = '<table border=0><tr><td class="table_title"> Alo </td></tr>';

	for (var row = 0; row < total_rows; row ++) {

		if (row == 0) {
			mytable += '<tr class="table_header_row">';
			mytable += '<td>Sub zone</td>';
		} else {
			mytable += '<tr>';
			mytable += '<td>' + info[0][row - 1]  + '</td>';
		}

		for (col of choices_indexes) {
			mytable += '<td>' + info[row+1][col]  + '</td>';
		}

		mytable += '</tr>';

	}

	mytable += '</table>';

	//document.getElementById('table_place').innerHTML = '<p>aaa</p>';
	document.getElementById('table_place').innerHTML = mytable;
};

function expandTable() {
  var tempo = [];
  var choices_indexes = [];
  var info = json_dict_full[current_dist];

  if (current_dist == "") {
  	document.getElementById('modal-body').innerHTML = "Please choose a district first";
  } else {
    for (choice in choices) {
      tempo = tempo.concat(mapping_dict[choices[choice]]);
    }

    for (index = 0; index < tempo.length; index++) {
      temp = info[1].findIndex(element => element == tempo[index]);
      if (temp > -1) choices_indexes.push(temp);
    }

    var mytable = '<table border=0><tr><td class="table_title">' + current_dist + '</td></tr>';

    for (var row = 0; row < total_rows; row ++) {
      if (row == 0) {
      	mytable += '<tr class="table_header_row">';
        mytable += '<td>Sub zone</td>';
      } else {
      	mytable += '<tr>';
        mytable += '<td>' + info[0][row - 1]  + '</td>';
      }

      for (col of choices_indexes) {
        mytable += '<td>' + info[row+1][col]  + '</td>';
      }

      mytable += '</tr>';
      
    }

    mytable += '</table>';
    document.getElementById('modal-body').innerHTML = mytable;
  }
}

/*_________________________________________________________*/
/*
* rwdImageMaps jQuery plugin v1.6
*
* Allows image maps to be used in a responsive design by recalculating the area coordinates to match the actual image size on load and window.resize
*
* Copyright (c) 2016 Matt Stow
* https://github.com/stowball/jQuery-rwdImageMaps
* http://mattstow.com
* Licensed under the MIT license
*/
;(function($) {
	$.fn.rwdImageMaps = function() {
		var $img = this;

		var rwdImageMap = function() {
			$img.each(function() {
				if (typeof($(this).attr('usemap')) == 'undefined')
					return;

				var that = this,
					$that = $(that);

				// Since WebKit doesn't know the height until after the image has loaded, perform everything in an onload copy
				$('<img />').on('load', function() {
					var attrW = 'width',
						attrH = 'height',
						w = $that.attr(attrW),
						h = $that.attr(attrH);

					if (!w || !h) {
						var temp = new Image();
						temp.src = $that.attr('src');
						if (!w)
							w = temp.width;
						if (!h)
							h = temp.height;
					}

					var wPercent = $that.width()/100,
						hPercent = $that.height()/100,
						map = $that.attr('usemap').replace('#', ''),
						c = 'coords';

					$('map[name="' + map + '"]').find('area').each(function() {
						var $this = $(this);
						if (!$this.data(c))
							$this.data(c, $this.attr(c));

						var coords = $this.data(c).split(','),
							coordsPercent = new Array(coords.length);

						for (var i = 0; i < coordsPercent.length; ++i) {
							if (i % 2 === 0)
								coordsPercent[i] = parseInt(((coords[i]/w)*100)*wPercent);
							else
								coordsPercent[i] = parseInt(((coords[i]/h)*100)*hPercent);
						}
						$this.attr(c, coordsPercent.toString());
					});
				}).attr('src', $that.attr('src'));
			});
		};
		$(window).resize(rwdImageMap).trigger('resize');

		return this;
	};
})(jQuery);