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

let planningJson = [];
let agentsJson = [];

let planningWeek = 0;

const periodeJour = ["matin", "soir", "nuit", "sve", "jca"];
const semaine = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"];

let rd = undefined;

function updatePlanning(reinitRedips=true) {
    // On vide la table
    if (rd) rd.clearTable("planning");
	
	// Pour chaque jour de la semaine
	for (let i = planningWeek*7; i < Math.min((planningWeek+1)*7, planningJson.length); i++) {
		// Pour chaque periode de la journée (matin, soir, nuit, sve ou jca)
		for (const [key, values] of Object.entries(planningJson[i])) {
			if (periodeJour.includes(key)) {
				const trjours = document.getElementById(key);
				const td = Array.from(trjours.children).find(child => child.className == semaine[i % 7]);
				// Pour chaque agent travaillant durant cette période
				for(let j = 0; j < values.length; j++) {
					const div = document.createElement("div");
					div.classList.add("redips-drag");
					div.textContent = values[j];
					td.append(div);
				}
			}
		}
	}
	if (reinitRedips) initRedips();
}

function updateAgents(reinitRedips=true) {
    // On vide la table
	const agentsTable = document.getElementById("agents");
	agentsTable.innerHTML = '';
	const tbody = document.createElement("tbody");

	// Numéros
	const numeroTR = document.createElement("tr");
	const numeroTH = document.createElement("th");
	numeroTH.classList.add("redips-rowhandler");
	numeroTH.textContent = "Numéro agent";
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
	pourcentageTH.textContent = "Pourcentage jours travaillés";
	pourcentageTR.append(pourcentageTH);

	for (let i = 0; i < agentsJson.length; i++) {		
		const pourcentageTD = document.createElement("td");
	    pourcentageTD.classList.add("redips-mark");
		pourcentageTD.textContent = agentsJson[i].pourcentage + '%';
		pourcentageTR.append(pourcentageTD);
	}
	tbody.append(pourcentageTR);
	agentsTable.append(tbody);
	if (reinitRedips) initRedips();
}

// A appeler à la toute fin de la fonction "init"
function initRedips() {
	rd = REDIPS.drag;
	rd.init();
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
		updatePlanning(false);
	}));
	const agentsPlanning = fetch("/agents_json").then(res => res.json().then(r => {
		agentsJson = r;
		updateAgents(false);
	}));
	Promise.all([promisePlanning, agentsPlanning]).then(() => initRedips());
	document.getElementById("previous").addEventListener('click', () => {
	    planningWeek = Math.max(0, planningWeek-1);
	    updatePlanning();
	});
	document.getElementById("next").addEventListener('click', () => {
	    planningWeek++;
	    updatePlanning();
	});
};

// add onload event listener
window.addEventListener('DOMContentLoaded', init);


