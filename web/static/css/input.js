document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    var formControls = document.querySelectorAll('.form-control');
    
    formControls.forEach(function(formControl) {
      formControl.addEventListener('input', function() {
        var field = this.closest('.form-group');
        
        if (this.value) {
          field.classList.add('field--not-empty');
        } else {
          field.classList.remove('field--not-empty');
        }
      });
    });
  });
  