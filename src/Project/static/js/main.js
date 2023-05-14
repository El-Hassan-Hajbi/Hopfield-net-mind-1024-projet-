document.addEventListener('DOMContentLoaded', function() {
function f(vector) {
    var res = [];
    for (var element of vector) {
      if (element == 0) {
          res[res.length] = -1;
      }
      else {
        res[res.length] = 1;
      }
    }
    return res;
  }

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

var csrftoken = getCookie('csrftoken');

async function load() {
    let response = await fetch('/load_data_view/');
    if (response.ok) { // if HTTP-status is 200-299
      // obtenir le corps de réponse (la méthode expliquée ci-dessous)
      let json_data = await response.json();
      return json_data;
    } else {
      alert("HTTP-Error: " + response.status);
    }
}

async function run_model() {
    let response = await fetch('/run_model_view/');

    if (response.ok) { // if HTTP-status is 200-299
      // obtenir le corps de réponse (la méthode expliquée ci-dessous)
      let json_data = await response.json();
      return json_data;
    } else {
      alert("HTTP-Error: " + response.status);
    }
}

async function classify_js(input, xtrain, ytrain) {
  var url = '/classify_view/';
  let data = {
    input: input,
    xtrain: xtrain,
    ytrain: ytrain
  };

  try {
    let response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken  // Include the CSRF token in the request headers
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      let json = await response.json();
      document.getElementById("output").innerHTML = json.result;
    } else {
      alert('HTTP-Error: ' + response.status);
    }
  } catch (error) {
    console.error('Fetch error:', error);
  }
}

async function noise_js(input) {
  var url = '/noise_view/';
  let data = {
    input: input,
  };

  try {
    let response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken  // Include the CSRF token in the request headers
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      let json = await response.json();
      return json;
    } else {
      alert('HTTP-Error: ' + response.status);
    }
  } catch (error) {
    console.error('Fetch error:', error);
  }
}

async function unnoise_js(input) {
  var url = '/unnoise_view/';
  let data = {
    input: input,
  };

  try {
    let response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken  // Include the CSRF token in the request headers
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      let json = await response.json();
      return json;
    } else {
      alert('HTTP-Error: ' + response.status);
    }
  } catch (error) {
    console.error('Fetch error:', error);
  }
}

function App() {
    this.model;
    this.Xtrain, this.Ytrain, this.Xtest, this.Ytest;
    this._inputdrawingsElement = document.getElementById('input-drawing');
    this._classificationdrawingsElement = document.getElementById('classification-drawing');
    var input_drawing = new Canvas();
    var classification_drawing = new Canvas();
    this.input_drawing = input_drawing;
    this.classification_drawing = classification_drawing;
    this._inputdrawingsElement.appendChild(input_drawing.element());
    var boutonClassification = document.getElementById('run-classification');
    var boutonRefreshtest = document.getElementById('refreshtest');
    var boutonRefreshtrain = document.getElementById('refreshtrain');
    var output_text = document.getElementById('output-classification');
    var self = this;

    let cpt = 1;
    let ptrain = 0;
    let ptest = 0;
    boutonRefreshtest.addEventListener('click', function(){
        input_drawing.setVector(f(self.Xtest[ptest]));
        ptest++;
    });

    boutonRefreshtrain.addEventListener('click', function(){
        input_drawing.setVector(f(self.Xtrain[ptrain]));
        ptrain++;
    });

    boutonClassification.addEventListener('click', async function(){
        var loadingBar = document.getElementById('progress-bar');

        try {
            // Show loading bar
            loadingBar.style.visibility = 'visible';

            const input = f(input_drawing.print_cells());
            await classify_js(input, self.Xtrain, self.Ytrain);

            // Complete loading bar
            loadingBar.style.animation = 'none';
            loadingBar.style.width = '100%';

            console.log('Request ended');
        } catch (error) {
        // Handle any errors that occurred during the request
            console.error(error);
        } finally {
            // Hide loading bar after a short delay for visibility
            setTimeout(function() {
              loadingBar.style.visibility = 'hidden';
            }, 500);
        }
    });

   document.getElementById('load').addEventListener('click', async function() {
      var loadingBar = document.getElementById('progress-bar');

      try {
        // Show loading bar
        loadingBar.style.visibility = 'visible';

        // Start the request
        let json_data = await load();
        self.Xtrain = json_data.Xtrain;
        self.Ytrain = json_data.Ytrain;
        self.Xtest = json_data.Xtest;
        self.Ytest = json_data.Ytest;
        self.model = await run_model();

        // Complete loading bar
        loadingBar.style.animation = 'none';
        loadingBar.style.width = '100%';

        console.log('Request ended');
      } catch (error) {
        // Handle any errors that occurred during the request
        console.error(error);
      } finally {
        // Hide loading bar after a short delay for visibility
        setTimeout(function() {
          loadingBar.style.visibility = 'hidden';
        }, 500);
      }
    });

    document.getElementById('noise').addEventListener('click', async function() {
      var loadingBar = document.getElementById('progress-bar');

      try {
        // Show loading bar
        loadingBar.style.visibility = 'visible';

        // Start the request

        const input = f(input_drawing.print_cells());
        let json_data = await noise_js(input);
        input_drawing.setVector(json_data.result);

        // Complete loading bar
        loadingBar.style.animation = 'none';
        loadingBar.style.width = '100%';

        console.log('Request ended');
      } catch (error) {
        // Handle any errors that occurred during the request
        console.error(error);
      } finally {
        // Hide loading bar after a short delay for visibility
        setTimeout(function() {
          loadingBar.style.visibility = 'hidden';
        }, 500);
      }
    });

    document.getElementById('unnoise').addEventListener('click', async function() {
      var loadingBar = document.getElementById('progress-bar');

      try {
        // Show loading bar
        loadingBar.style.visibility = 'visible';

        // Start the request
        const input = f(input_drawing.print_cells());
        let json_data = await unnoise_js(input);
        input_drawing.setVector(json_data.result);

        // Complete loading bar
        loadingBar.style.animation = 'none';
        loadingBar.style.width = '100%';

        console.log('Request ended');
      } catch (error) {
        // Handle any errors that occurred during the request
        console.error(error);
      } finally {
        // Hide loading bar after a short delay for visibility
        setTimeout(function() {
          loadingBar.style.visibility = 'hidden';
        }, 500);
      }
    });
}

new App();

});
