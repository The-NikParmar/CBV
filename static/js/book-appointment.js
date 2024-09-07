function fetchDiseases(doctorId) {
    if (!doctorId) {
        $('#id_disease').html('<option value="">Select a Disease</option>');
        return;
    }
    
    $.ajax({
        url: "{% url 'patient:get_diseases' %}",
        data: { doctor_id: doctorId },
        success: function(data) {
            var diseaseSelect = $('#id_disease');
            diseaseSelect.html('<option value="">Select a Disease</option>');
            
            $.each(data.diseases, function(index, disease) {
                diseaseSelect.append(
                    $('<option>', { 
                        value: disease.id, 
                        text: disease.problem_name,
                        'data-duration': disease.time_required
                    })
                );
            });
        },
        error: function(xhr, errmsg, err) {
            console.error('Error fetching diseases:', errmsg);
            console.error('Response:', xhr.responseText); 
        }
    });
}

function fetchAvailableSlots(doctorId, date, diseaseId) {
  $.ajax({
      url: "{% url 'patient:get_available_slots' %}",
      data: {
          doctor_id: doctorId,
          appointment_date: date,
          disease_id: diseaseId
      },
      success: function(data) {
          var slotSelect = $('#id_appointment_time');
          slotSelect.html('<option value="">Select a Time</option>');

          if (data.slots) {
              $.each(data.slots, function(index, slot) {
                  slotSelect.append(
                      $('<option>', { value: slot, text: slot })
                  );
              });
          } else {
              console.error('No slots data received');
          }
      },
      error: function(xhr, errmsg, err) {
          console.error('Error fetching slots:', errmsg);
          console.error('Response:', xhr.responseText); // Log the response text for debugging
      }
  });
}

$(document).ready(function() {
  $('#id_doctor, #id_appointment_date, #id_disease').change(function() {
      var doctorId = $('#id_doctor').val();
      var date = $('#id_appointment_date').val();
      var diseaseId = $('#id_disease').val();

      if (doctorId && date && diseaseId) {
          fetchAvailableSlots(doctorId, date, diseaseId);
      }
  });
});
    
  document.addEventListener('DOMContentLoaded', function() {
    var today = new Date().toISOString().split('T')[0];
    document.getElementById('{{ form.appointment_date.id_for_label }}').setAttribute('min', today);
});