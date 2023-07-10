from cards import mana_artifacts, mana_providers
from deck_helpers import get_land_count, Deck


# This is terribly static and needs to be made dynamic.
# Eg, allow it to get a decklist from moxfield or something and load everything dynamically
deck_size = 99
turn = 2
lands = 25

mana_crypt = 1
sol_ring = 1
mana_vault = 1
grim_monolith = 0
chrome_mox = 1
mox_diamond = 1
mox_amber = 1  # Assumes you always have the legendary creature, i.e. Rograkh decks
mox_opal = 1
lotus_petal = 1
arcane_signet = 1
paradise_mantle = 1  # Assumes you always have the Rograkh
springleaf_drum = 1  # Assumes you always have the Rograkh
dark_ritual = 1
culling_the_weak = 1  # Assumes you always have a creature
cabal_ritual = 1  # Assumes you don't have threshold
simian_spirit_guide = 1
ragavan = 1  # Assumes you can always hit someone
infernal_plunge = 1  # Assumes you always have a creature
jeskas_will = 1  # Assumes largest opposing hand size is 5
rite_of_flame = 1
dockside_extortionist = 1  # Assumes Dockside generates 4 treasures and you are casting it the turn you need the mana
strike_it_rich = 1
artifact_dud = 3

non_mana = deck_size - lands - artifact_dud - mana_crypt - sol_ring - mana_vault - grim_monolith - chrome_mox - mox_diamond - mox_amber - mox_opal - lotus_petal - arcane_signet - paradise_mantle - springleaf_drum - dark_ritual - culling_the_weak - cabal_ritual - simian_spirit_guide - ragavan - infernal_plunge - jeskas_will - rite_of_flame - dockside_extortionist - strike_it_rich

deck = ['dud'] * (non_mana) + ['land'] * (lands) + ['artifact_dud'] * (artifact_dud) + ['Mana Crypt'] * (mana_crypt) + [
    'Sol Ring'] * (sol_ring) + ['Mana Vault'] * (mana_vault) + ['Grim Monolith'] * (grim_monolith) + ['Chrome Mox'] * (
           chrome_mox) + ['Mox Diamond'] * (mox_diamond) + ['Mox Amber'] * (mox_amber) + ['Mox Opal'] * (mox_opal) + [
           'Lotus Petal'] * (lotus_petal) + ['Arcane Signet'] * (arcane_signet) + ['Paradise Mantle'] * (
           paradise_mantle) + ['Springleaf Drum'] * (springleaf_drum) + ['Dark Ritual'] * (dark_ritual) + [
           'Culling the Weak'] * (culling_the_weak) + ['Cabal Ritual'] * (cabal_ritual) + ['Simian Spirit Guide'] * (
           simian_spirit_guide) + ['ragavan'] * (ragavan) + ['infernal plunge'] * (infernal_plunge) + [
           'Infernal Plunge'] * (infernal_plunge) + ['Jeskas Will'] * (jeskas_will) + ['Rite of Flame'] * (
           rite_of_flame) + ['Dockside Extortionist'] * (dockside_extortionist) + ['Strike It Rich'] * (
           strike_it_rich)  # Creates the deck


def simulate_hand(deck_list, num_turns=3, max_mulligans=3, min_lands_to_mulligan=1, max_num_lands_to_mulligan=3):
    # copy and shuffle the deck
    current_deck = Deck(deck_list)

    # get a random starting hand
    starting_hand = current_deck.draw(7)

    # Calculate the number of lands in your hand
    available_lands = get_land_count(starting_hand)

    # resolve mulligans
    num_mulligans = 0
    if max_mulligans > 0:
        while num_mulligans <= max_mulligans:
            if available_lands < min_lands_to_mulligan or available_lands > max_num_lands_to_mulligan:
                # first one is free (7-0), the rest are one card less each mulligan
                current_deck = Deck(deck_list)
                starting_hand = current_deck.draw(7-num_mulligans)
                available_lands = get_land_count(starting_hand)
                if min_lands_to_mulligan <= available_lands <= max_num_lands_to_mulligan:
                    # we landed between min and max, so we're good and can break out of the while loop
                    break
            num_mulligans += 1

    # Calculate the number of artifacts in your opening hand. This matters for some mana producing cards like moxes
    starting_total_artifacts = 0
    for x in starting_hand:
        if x in mana_artifacts:
            starting_total_artifacts += 1
    # adds in the number of non-mana producing artifacts in hand
    starting_total_artifacts += starting_hand.count('artifact_dud')

    # We remove one time use mana cards from the
    available_mana, temp_mana = calculate_starting_mana(starting_hand, starting_total_artifacts)

    # For each turn we draw a card and add producible mana if it is a mana producing card
    current_turn = 1
    turn_data = {}
    while current_turn <= num_turns:
        drawn_card = current_deck.draw(1)[0]
        if drawn_card in mana_providers:
            card = mana_providers[drawn_card]
            if card.tags and "single_use" in card.tags:
                temp_mana += card.mana_produced
            else:
                available_mana += card.mana_produced
        elif drawn_card == "land":
            available_lands += 1
            available_mana += 1

        turn_data[f"turn_{str(current_turn)}"] = {
            "available_lands": available_lands,
            "available_mana": available_mana,
            "temp_mana": temp_mana
        }
        current_turn += 1

    return turn_data


def calculate_starting_mana(current_hand, num_artifacts):
    cards_in_hand = len(current_hand)
    starting_total_mana = 0
    temp_mana_total = 0
    starting_lands = get_land_count(current_hand)
    starting_total_mana += starting_lands
    cards_to_check_for_cost = []
    for card in current_hand:
        if card in mana_providers:
            card_data = mana_providers[card]
            if card_data.cmc > 0:
                cards_to_check_for_cost.append(card)
            else:
                starting_total_mana += card_data.mana_produced
    for card in cards_to_check_for_cost:
        card_data = mana_providers[card]
        # handle cards with special cases. This is not scalable at all!
        if card == "Mox Diamond":
            if starting_lands == 0:
                continue
                # starting_total_mana += card_data.get("mana_produced")
        elif card == "Chrome Mox":
            # Check to make sure we have at least one non-artifact, non-land card in our hand.
            if (num_artifacts + starting_lands) == cards_in_hand:
                continue
        elif card == "Mox Opal":
            if num_artifacts < 3:
                continue
        elif card_data.cmc > starting_total_mana:
            # Things that have a casting cost should have that cost subtracted from the mana the produce if we're
            # talking about starting total mana here. They may produce more later, like paradise mantle or springleaf
            # but that's not factored into starting available mana
            continue
        if card_data.tags and "single_use" in card_data.tags:
            temp_mana_total = card_data.mana_produced - card_data.cmc
        else:
            starting_total_mana += card_data.mana_produced - card_data.cmc

    return starting_total_mana, temp_mana_total


num_simulations = 100000  # The total number of hand simulations you want to run. Could make this a user input.
sim_results = []
for _ in range(num_simulations):
    result_data = simulate_hand(deck, 5)
    sim_results.append(result_data)

print(result_data)
# TODO: Add average calculations for all sims
# average_mana = grand_total_mana / num_simulations  # Calculates the average mana available by the designated turn.
#
# average_lands = grand_total_lands / num_simulations
#
# percent_no_lands = (no_lands / num_simulations) * 100
#
# average_mana_no_lands = mana_no_lands / no_lands
#
# percent_one_land = (one_land / num_simulations) * 100
#
# average_mana_one_land = mana_one_land / one_land
#
# percent_two_lands = (two_lands / num_simulations) * 100
#
# average_mana_two_lands = mana_two_lands / two_lands
#
# percent_three_lands = (three_lands / num_simulations) * 100
#
# average_mana_three_lands = mana_three_lands / three_lands
#
# percent_four_plus_lands = (four_plus_lands / num_simulations) * 100
#
# if four_plus_lands != 0:
#     average_mana_four_plus_lands = mana_four_plus_lands / four_plus_lands
#
# percent_mulligans = (grand_total_mulligans / grand_total_hands) * 100
#
# percent_first_seven = (grand_total_first_seven / num_simulations) * 100
#
# percent_second_seven = (grand_total_second_seven / num_simulations) * 100
#
# percent_six = (grand_total_six / num_simulations) * 100
#
# percent_five = (grand_total_five / num_simulations) * 100
#
# percent_four = (grand_total_four / num_simulations) * 100
#
# percent_three = (grand_total_three / num_simulations) * 100
#
# print("Average mana across 100,000 simulations:", round(average_mana,
#                                                         2))  # Prints the average available mana on the designated turn rounded to two decimal places. Could add something here to remind you of the land count, deck size, and turns you specified.
#
# print("Percentage of hands mulliganned across 100,000 simulations:", round(percent_mulligans, 1))
#
# print("Percentage of first seven-card hands kept:", round(percent_first_seven, 1))
#
# print("Percentage of second seven-card hands kept:", round(percent_second_seven, 1))
#
# print("Percentage of six-card hands kept:", round(percent_six, 1))
#
# print("Percentage of five-card hands kept:", round(percent_five, 1))
#
# print("Percentage of four-card hands kept:", round(percent_four, 1))
#
# print("Percentage of three-card hands kept:", round(percent_three, 1))
#
# print("Average lands across 100,000 simulations:", round(average_lands, 2))
#
# print("Percentage of 100,000 simulations with no lands drawn:", round(percent_no_lands, 1))
#
# print("Average mana with no lands drawn:", round(average_mana_no_lands, 2))
#
# print("Percentage of 100,000 simulations with one land drawn:", round(percent_one_land, 1))
#
# print("Average mana with one land drawn:", round(average_mana_one_land, 2))
#
# print("Percentage of 100,000 simulations with two lands drawn:", round(percent_two_lands, 1))
#
# print("Average mana with two lands drawn:", round(average_mana_two_lands, 2))
#
# print("Percentage of 100,000 simulations with three lands drawn:", round(percent_three_lands, 1))
#
# print("Average mana with three lands drawn:", round(average_mana_three_lands, 2))
#
# print("Percentage of 100,000 simulations with four or more lands drawn:", round(percent_four_plus_lands, 1))
#
# if four_plus_lands != 0:
#     print("Average mana with four or more lands drawn:", round(average_mana_four_plus_lands, 2))