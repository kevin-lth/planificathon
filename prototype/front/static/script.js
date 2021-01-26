/* eslint-env browser, jquery */
/* eslint
   semi: ["error", "always"],
   indent: [2, "tab"],
   no-tabs: 0,
   no-multiple-empty-lines: ["error", {"max": 2, "maxEOF": 1}],
   one-var: ["error", "always"] */
/* global REDIPS */

/* enable strict mode */
'use strict';


// create redips container
let redips = {};

const agentsNumber = 10;
var planningJson = [];
var agentsJson = [];
const periodeJour = ["matin", "soir", "nuit", "sve", "jca"];
const semaine = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"];

function fillPlanning(){
	console.log(planningJson);
	console.log(agentsJson);
	
	// Pour chaque jour de la semaine
	for(let i = 0; i < 7; i++){
		// Pour chaque periode de la journée (matin, soir, nuit, sve ou jca)
		for(const [key, values] of Object.entries(planningJson[i])) {
			if(periodeJour.includes(key)) {
				// Pour chaque agent travaillant durant cette période
				for(let j = 0; j < values.length; j++) {
					const trjours = document.getElementById(key);
					var td = Array.from(trjours.children).find(child => child.className == semaine[i]);
					
					if(td.innerText === "") {
						td.innerHTML = `<div class="redips-drag">`+ values[j] +`</div>`;
					}
					else {
						const a = td.innerText.split("\n");
						td.innerHTML = `<div class="redips-drag">`+ values[j] +`</div>`;
						for(let k = 0; k < a.length; k++) {
							td.innerHTML += `<div class="redips-drag">`+ a[k] +`</div>`;
						}
					}
				}
			}
		}
	}
}

function fillAgents() {
	var agentsTable = document.getElementById("agents");

	const colGroup = document.createElement("colgroup");
	const tbody = document.createElement("tbody");
	let col = document.createElement("col");
	col.width = 100;
	colGroup.append(col);

	// Numéros
	let trnumero = document.createElement("tr");
	let numeroTD = document.createElement("td");
	numeroTD.innerHTML = `<div class="redips-mark">Numéro agent</div>`;
	trnumero.append(numeroTD);
	tbody.append(trnumero);
	for(let i = 0; i < agentsJson.length; i++) {
		let col = document.createElement("col");
		col.width = 100;
		colGroup.append(col);
		let numeroTD = document.createElement("td");
		numeroTD.innerHTML = `<div class="redips-drag redips-clone">`+ agentsJson[i].numero +`</div>`;
		trnumero.append(numeroTD);
		tbody.append(trnumero);
	}

	// Pourcentages
	let tr = document.createElement("tr");
	let td = document.createElement("td");
	td.innerHTML = `<div class="redips-mark">Pourcentage jours travaillés</div>`;
	tr.append(td);
	tbody.append(tr);

	for(let i = 0; i < agentsJson.length; i++) {		
		let pourcentageTD = document.createElement("td");
		pourcentageTD.innerHTML = `<div class="redips-mark">`+ agentsJson[i].pourcentage +`%</div>`;
		tr.append(pourcentageTD);
		tbody.append(tr);
	}

	agentsTable.append(colGroup);
	agentsTable.append(tbody);
}

// A appeler à la toute fin de la fonction redips.init
function redipsInit() {
	let rd = REDIPS.drag;
	rd.init();
	rd.event.dropped = function (targetCell) {
		console.log(targetCell);
		console.log(targetCell.className);
		console.log(targetCell.parentElement.id);
		console.log(targetCell.innerText.split("\n"));
	}
}

redips.init = function () {

	fetch("http://localhost:8000/planning_json")
	.then(res => res.json().then(r => {
		planningJson = r;
		fetch("http://localhost:8000/agents_json")
		.then(res => res.json().then(r => {
			agentsJson = r;
			fillPlanning();
			fillAgents();

			redipsInit();
		}))
	}));
};


// add onload event listener
if (window.addEventListener) {
	window.addEventListener('load', redips.init, false);
}
else if (window.attachEvent) {
	window.attachEvent('onload', redips.init);
}

