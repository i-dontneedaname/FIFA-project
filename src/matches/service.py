from fastapi import HTTPException, status

from src.players.dependencies import get_player_or_404
from src.utils.service_manager import IServiceManager
from src.matches.schemas import MatchResult


class MatchesService:

    async def add_match(
            self,
            service_manager: IServiceManager,
            response_schema,
            data: dict,
            owner_id
    ):
        async with service_manager:
            await self.validate_players_of_match(service_manager, data['first_team']['player_id'],
                                                 data['second_team']['player_id'], owner_id)
            last_match_id = await service_manager.matches.get_last_match_id()
            first_team = await service_manager.matches.add_one({
                'id': last_match_id + 1,
                'date': data['date'],
                'minutes': data['minutes'],
                'seconds': data['seconds'],
                **data['first_team']
            })

            second_team = await service_manager.matches.add_one({
                'id': last_match_id + 1,
                'date': data['date'],
                'minutes': data['minutes'],
                'seconds': data['seconds'],
                **data['second_team']
            })

            await service_manager.commit()
            concatenated_match = self.concatenate_match(response_schema, [first_team, second_team])
            return concatenated_match


    async def get_matches(
            self,
            service_manager: IServiceManager,
            response_schema,
            pagination,
    ):
        async with service_manager:
            concatenated_matches_list = []
            matches_dict = {}

            matches_list = await service_manager.matches.find_all(pagination)

            if len(matches_list):
                for match in matches_list:
                    if match.id in matches_dict:
                        matches_dict[match.id].append(match)
                    else:
                        matches_dict[match.id] = [match]

                for k in matches_dict.keys():
                    concatenated_match = self.concatenate_match(response_schema, matches_dict[k])
                    concatenated_matches_list.append(concatenated_match)

                return concatenated_matches_list

            else:
                return []

    async def get_match(
            self,
            service_manager: IServiceManager,
            response_schema,
            id: int
    ):
        async with service_manager:
            one_match_list = await service_manager.matches.find_all(id=id)
            concatenated_match = self.concatenate_match(response_schema, one_match_list)
            return concatenated_match

    def concatenate_match(
            self,
            response_schema,
            one_match_list
    ):

        return response_schema(
            id=one_match_list[0].id,
            date=one_match_list[0].date,
            minutes=one_match_list[0].minutes,
            seconds=one_match_list[0].seconds,
            first_team=MatchResult(
                player=one_match_list[0].player,
                victory=one_match_list[0].victory,
                goals=one_match_list[0].goals,
                ball_possession=one_match_list[0].ball_possession,
                strikes=one_match_list[0].strikes,
                xg=one_match_list[0].xg,
                passes=one_match_list[0].passes,
                selections=one_match_list[0].selections,
                successful_selections=one_match_list[0].successful_selections,
                interceptions=one_match_list[0].interceptions,
                saves=one_match_list[0].saves,
                violations=one_match_list[0].violations,
                offsides=one_match_list[0].offsides,
                corners=one_match_list[0].corners,
                free_kicks=one_match_list[0].free_kicks,
                penalty_kicks=one_match_list[0].penalty_kicks,
                yellow_cards=one_match_list[0].yellow_cards,
                red_cards=one_match_list[0].red_cards,
            ),
            second_team=MatchResult(
                player=one_match_list[1].player,
                victory=one_match_list[1].victory,
                goals=one_match_list[1].goals,
                ball_possession=one_match_list[1].ball_possession,
                strikes=one_match_list[1].strikes,
                xg=one_match_list[1].xg,
                passes=one_match_list[1].passes,
                selections=one_match_list[1].selections,
                successful_selections=one_match_list[1].successful_selections,
                interceptions=one_match_list[1].interceptions,
                saves=one_match_list[1].saves,
                violations=one_match_list[1].violations,
                offsides=one_match_list[1].offsides,
                corners=one_match_list[1].corners,
                free_kicks=one_match_list[1].free_kicks,
                penalty_kicks=one_match_list[1].penalty_kicks,
                yellow_cards=one_match_list[1].yellow_cards,
                red_cards=one_match_list[1].red_cards,
            )
        )

    async def validate_players_of_match(
            self,
            service_manager: IServiceManager,
            player1_id,
            player2_id,
            owner_id
    ):
        if player1_id == player2_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        player_1 = await get_player_or_404(service_manager, player1_id)
        player_2 = await get_player_or_404(service_manager, player2_id)

        if player_1.owner_id != owner_id or player_2.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
