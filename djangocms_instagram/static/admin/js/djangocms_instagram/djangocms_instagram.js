function showInstagramLookupPopup(triggeringLink, accountID) {
  var name = triggeringLink.id.replace('lookup_id_', ''),
    url = triggeringLink.href + '&_popup=1';

  if (accountID) {
    url += '&account=' + accountID;
    var win = window.open(url, name, 'height=700,width=800,resizable=yes,scrollbars=yes');
    win.focus();
  } else {
    alert('A connected Instagram account is required for\n' + triggeringLink.title + '.');
  }
  return false;
}

function dismissInstagramLookupPopup(win, chosenId, chosenLabel) {
  var input = document.getElementById('id_' + win.name);
  if (input) {
    input.value = chosenId;
  }
  var label = document.getElementById('label_' + win.name);
  if (label) {
    label.innerHTML = chosenLabel;
  }
  win.close();
}

(function($) {
  $(function() {
    function toggleSource() {
      var source = $('input[name="source"]:checked').val();
      $('.field-user_id, .field-location_id, .field-hashtag').removeClass('required').hide();

      switch (source) {
        case 'feed':
          $('.field-user_id').show();
          break;
        case 'tag':
          $('.field-hashtag').addClass('required').show();
          break;
        case 'location':
          $('.field-location_id').addClass('required').show();
          break;
      }
    }

    $('input[name="source"]').change(function() {
      toggleSource();
    });

    toggleSource();

    $('.instagram-search').click(function(e) {
      e.preventDefault();
      var triggeringLink = this,
        accountID = $('input[name="account"]').val() || 0;
      showInstagramLookupPopup(triggeringLink, accountID);
    });
  });
})(django.jQuery);
