Dans agent.json il y a une liste de chaque agent avec dedans :
   - **numéro** :: *int*      : l'id de l'agent
   - **pourcentage** :: *int*       : le "pourcentage" de temps plein de l'agent
   - **matin** :: *list d'int*      : une liste dont chaque case correspond à un jour (de lundi à dimanche) 
   avec un 1 si l'agent est assigné à ce matin et un 0 sinon
   - **soir** :: *list d'int*      : une liste dont chaque case correspond à un jour (de lundi à dimanche) 
   avec un 1 si l'agent est assigné à ce soir et un 0 sinon
   - **nuit** :: *list d'int*      : une liste dont chaque case correspond à un jour (de lundi à dimanche) 
   avec un 1 si l'agent est assigné à cette nuit et un 0 sinon
   - **jca** :: *list d'int*      : une liste dont chaque case correspond à un jour (de lundi à dimanche) 
   avec un 1 si l'agent est assigné à cette sve et un 0 sinon
   - **jca** :: *list d'int*      : une liste dont chaque case correspond à un jour (de lundi à dimanche) 
   avec un 1 si l'agent est assigné à cette jca et un 0 sinon


Dans planning.json il y a une liste des jours (de lundi à dimanche) contenant pour chaque jour :
   - **besoin_matin**  :: *int*     : Nombre de personnes nécessaire pour le matin
   - **besoin_soir**  :: *int*     : Nombre de personnes nécessaire pour le soir
   - **besoin_nuit**  :: *int*     : Nombre de personnes nécessaire pour la nuit
   - **besoin_sve**  :: *int*     : Nombre de personnes nécessaire pour la sve
   - **nb_jca**  :: *int*     : Nombre de personnes nécessaire pour la jca
   - **matin**  :: *list d'int*     : Id des agents assignés pour le matin
   - **soir**  :: *list d'int*     : Id des agents assignés pour le soir
   - **nuit**  :: *list d'int*     : Id des agents assignés pour la nuit
   - **sve**  :: *list d'int*     : Id des agents assignés pour la sve
   - **jca**  :: *list d'int*     : Id des agents assignés pour la jca
