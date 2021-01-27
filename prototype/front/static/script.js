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
let alertes = {};
let indicateurs = {};

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

function exportPlanning(sendToServer=false) {
    if (rd) {
        const content = JSON.parse(rd.saveContent("planning", "json"));
	    for (let i = planningWeek*7; i < Math.min((planningWeek+1)*7, planningJson.length); i++) {
	        for (let j = 0; j < periodeJour.length; j++) planningJson[i][periodeJour[j]] = [];
		}
	    for (let i = 0; i < content.length; i++) {
	        const x = content[i][1];
	        const y = content[i][2];
			const n = content[i][4];
	        planningJson[planningWeek*7 + y-1][periodeJour[x-1]].push(parseInt(n));
		}

		// for(let i = 0; i < agentsJson.length; i++) {
		// 	for(let j = 0; j < agentsJson[i]["jca"].length; j++) {
		// 		for(let k = 0; k < planningJson.length; k++) {
					
		// 		}
		// 		// console.log(agentsJson[i]["jca"][j]);		
		// 	}
		// }

		// TODO: sendToServer
		fetch('/update_planning', {
			method: 'PUT',
			headers: {
			'Content-Type': 'application/json'
			},
			body: JSON.stringify(planningJson)
		}).then(res => res.json().then(r => {
			alertes = r["contraintes"];
			indicateurs = r["indicateurs"];
			const indicateurCreneau = document.getElementById("indicateur-creneau");
			const alerteBesoins = document.getElementById("alerte-besoins");
			const indicateurJca = document.getElementById("indicateur-jca");
			indicateurCreneau.innerHTML = `Equitable pénibilité : <b>`+ indicateurs.equiteCreneau[0][0] +`</b>`
			alerteBesoins.innerHTML = `Il reste des personnes à attribuer : <b>`+ alertes.besoins[0] +`</b>`
			indicateurJca.innerHTML = `Equitable jca : <b>`+ indicateurs.equiteJca[0] +`</b>`
		}));
    } else return [];
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
		numeroTD.innerHTML = `<div class="redips-drag redips-clone">${agentsJson[i].numero}</div>`;
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
	if (!rd) rd = REDIPS.drag;
	rd.init();
	rd.event.dropped = () => exportPlanning();
}

function init() {
	const upload_form = document.getElementById("upload_form");
	upload_form.addEventListener('submit', (e) => {
	    e.preventDefault();
	    e.stopPropagation();
        const form_data = new FormData(upload_form);
        fetch(upload_form.action, {
            method: upload_form.method,
            body: form_data
        }).then(response => response.json())
          .then(result => {
            console.log(result, result.planning, result.agents);
            planningJson = result.planning;
            agentsJson = result.agents;
		    updatePlanning(false);
		    updateAgents();
        });
	});
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


