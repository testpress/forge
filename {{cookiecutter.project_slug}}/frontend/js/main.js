// frontend/js/main.js
//
{% if cookiecutter.use_preline == 'y' %}
import { HSStaticMethods } from 'preline/non-auto';

document.addEventListener('DOMContentLoaded', () => {
  HSStaticMethods.autoInit();
});
{% endif %}
