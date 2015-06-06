(function($) {
  $(function() {
    var searchForm = $('#search-form'),
      queryInput = $('input[name="location"]', searchForm),
      latitudeInput = $('input[name="lat"]', searchForm),
      longitudeInput = $('input[name="lng"]', searchForm);

    function populateFormFields(latLng) {
      latitudeInput.val(latLng.lat());
      longitudeInput.val(latLng.lng());
      searchForm.submit();
    }

    queryInput.geocomplete({
        map: '#gmap',
        location: [latitudeInput.val(), longitudeInput.val()],
        markerOptions: {
          draggable: true
        },
        details: '#search-form'
      })
      .bind('geocode:result', function(event, result) {
        populateFormFields(result.geometry.location);
      })
      .bind('geocode:dragged', function(event, latLng) {
        populateFormFields(latLng);
        queryInput.val('');
      })
      .bind('geocode:error', function(event, status) {
        alert('Error: ' + status);
      })
      .bind('geocode:multiple', function(event, results) {
        populateFormFields(results[0].geometry.location);
      });
  });
})(django.jQuery);
