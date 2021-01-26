/* eslint-env browser, jquery */
/* eslint
   semi: ["error", "always"],
   indent: [2, "tab"],
   no-tabs: 0,
   no-multiple-empty-lines: ["error", {"max": 2, "maxEOF": 1}],
   one-var: ["error", "always"] */
/* global REDIPS */

/* enable strict mode */
"use strict";

const agentsNumber = 10;
var planningJson = [];
var agentsJson = [];
const periodeJour = ["matin", "soir", "nuit", "sve", "jca"];
const semaine = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"];

function updatePlanning(){
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

function updateAgents() {
	const agentsTable = document.getElementById("agents");
	const tbody = document.createElement("tbody");

	// Numéros
	const numeroTR = document.createElement("tr");
	const numeroTH = document.createElement("th");
	numeroTH.classList.add("redips-rowhandler");
	numeroTH.innerHTML = "Numéro agent";
	numeroTR.append(numeroTH);
	tbody.append(numeroTR);
	
	for (let i = 0; i < agentsJson.length; i++) {
		const numeroTD = document.createElement("td");
	    numeroTD.classList.add("redips-mark");
		numeroTD.innerHTML = `<div class="redips-drag redips-clone">`+ agentsJson[i].numero +`</div>`;
		numeroTR.append(numeroTD);
	}
	tbody.append(numeroTR);

	// Pourcentages
	let pourcentageTR = document.createElement("tr");
	let pourcentageTH = document.createElement("th");
	pourcentageTH.classList.add("redips-rowhandler");
	pourcentageTH.innerHTML = "Pourcentage jours travaillés";
	pourcentageTR.append(pourcentageTH);

	for (let i = 0; i < agentsJson.length; i++) {		
		const pourcentageTD = document.createElement("td");
	    pourcentageTD.classList.add("redips-mark");
		pourcentageTD.innerHTML = agentsJson[i].pourcentage + '%';
		pourcentageTR.append(pourcentageTD);
	}
	tbody.append(pourcentageTR);
	agentsTable.append(tbody);
}

// A appeler à la toute fin de la fonction "init"
function initRedips() {
	const rd = REDIPS.drag;
	rd.init();
	console.log(rd.saveContent("planning", "json")); // TODO
	rd.event.dropped = function (targetCell) {
		console.log(targetCell);
		console.log(targetCell.className);
		console.log(targetCell.parentElement.id);
		console.log(targetCell.innerText.split("\n"));
	}
}

function init() {
	const promisePlanning = fetch("/planning_json").then(res => res.json().then(r => {
		planningJson = r;
		updatePlanning();
	}));
	const agentsPlanning = fetch("/agents_json").then(res => res.json().then(r => {
		agentsJson = r;
		updateAgents();
	}));
	Promise.all([promisePlanning, agentsPlanning]).then(() => initRedips());
};

// add onload event listener
window.addEventListener('DOMContentLoaded', init);


