#-------------------------------------------------------------------------------
# Name:        Spatial Reasoning
# Purpose:     This module produces a model for spatial reasoning. It is
# based on the LISP code for Spatial Reasoning by PN Johnson Laird and R.Byrne,
# developed for their 1991 book 'Deduction' and their 1989 paper 'Spatial
# Reasoning.

# Author:      Ashwath Sampath
# Based on: http://mentalmodels.princeton.edu/programs/space-6.lisp
# Created:     09-04-2018
# Copyright:   (c) Ashwath Sampath 2018
#-------------------------------------------------------------------------------
""" Module which creates a model for spatial reasoning, based on
LISP code developed by PN Johnson-Laird and R.Byrne as part of their
1991 book 'Deduction' and their 1989 paper 'Spatial Reasoning'.  """
import sys
import argparse
from spatial_parser import SpatialParser
import spatial_array
import utilities
import model_validation
import model_builder
import model_combination
PARSER = SpatialParser()

class SpatialReasoning():
    """ This is a class used to implement the spatial reasoning model detailed
    by Johnson-Laird and Byrne in their 1991 book 'Deduction' """

    def __init__(self):
        """ Global variables declared, sample problems defined here"""

        # Create problems as a dictionary of dictionaries: just to satisfy
        # pylint.

        self.problems = {
            # Problems which need models to be combined
            'combination': {
                1: [["the square is behind the circle"],
                    ["the cross is in front of the triangle"],
                    ["the square is on the left of the cross"]],
                2: [["the circle is in front of the square"],
                    ["the triangle is behind the cross"],
                    ["the cross is on the right of the square"]],
                3: [["the square is behind the circle"],
                    ["the triangle is behind the cross"],
                    ["the cross is on the left of the square"]],
                4: [["the square is behind the circle"],
                    ["the triangle is behind the cross"],
                    ["the line is above the triangle"],
                    ["the cross is on the left of the square"]]
                },

            # Problems with a deductive conclusion
            # Problem 7: Prism 1, Problem 8: Prism 2, Problem 9: Prism 4
            'deductive': {
                1: [["the cross is in front of the circle"],
                    ["the circle is in front of the triangle"],
                    ["the cross is in front of the triangle"]],
                2: [["the triangle is on the right of the square"],
                    ["the circle is in front of the square"],
                    ["the cross is on the left of the square"],
                    ["the line is in front of the cross"],
                    ["the line is on the right of the ell"],
                    ["the star is in front of the ell"],
                    ["the circle is on the left of the vee"],
                    ["the ess is in front of the vee"],
                    ["the star is on the left of the ess"]],
                3: [["the square is on the right of the circle"],
                    ["the circle is on the right of the triangle"],
                    ["the square is on the right of the triangle"]],
                4: [["the square is on the right of the circle"],
                    ["the triangle is on the left of the circle"],
                    ["the square is on the right of the triangle"]],
                5: [["the circle is on the right of the square"],
                    ["the triangle is on the left of the circle"],
                    ["the cross is in front of the triangle"],
                    ["the star is in front of the circle"],
                    ["the cross is on the left of the star"]],
                6: [["the square is on the right of the circle"],
                    ["the cross is in front of the triangle"],
                    ["the triangle is on the left of the square"],
                    ["the square is behind the line"],
                    ["the line is on the right of the cross"]],
                7: [["the square is on the left of the triangle"],
                    ["the circle is on the right of the triangle"],
                    ["the circle is on the left of the cross"],
                    ["the cross is on the left of the star"],
                    ["the triangle is on the left of the star"]],
                8: [["the square is on the left of the triangle"],
                    ["the circle is on the right of the triangle"],
                    ["the triangle is on the left of the cross"],
                    ["the cross is on the left of the star"],
                    ["the triangle is on the left of the star"]],
                9: [["the square is on the right of the circle"],
                    ["the triangle is on the left of the square"],
                    ["the cross is in front of the triangle"],
                    ["the star is in front of the square"],
                    ["the star is on the right of the cross"]],
                10: [["the circle is on the right of the square"],
                     ["the triangle is on the left of the square"],
                     ["the cross is in front of the triangle"],
                     ["the star is in front of the square"],
                     ["the cross is on the left of the star"]],
                },
            # Spatially indeterminate problems: 1 is true, but needn't be.
            # 2 to 9 are false, but needn't be.
            # Reordered so that the 9-premise problem 2 in the Lisp code now
            # sits at problem 6. The other premises each move up a step.
            # 6-8 are included only because they were included in the Lisp
            # code. It's impossible for a human reasoner to solve these problems
            'indeterminate': {
                1: [["the circle is on the right of the square"],
                    ["the triangle is on the left of the circle"],
                    ["the cross is in front of the triangle"],
                    ["the line is in front of the square"],
                    ["the cross is on the left of the line"]],
                2: [["the square is on the right of the circle"],
                    ["the triangle is on the left of the square"],
                    ["the triangle is on the right of the circle"]],
                3: [["the square is on the right of the circle"],
                    ["the triangle is on the left of the square"],
                    ["the cross is in front of the triangle"],
                    ["the line is in front of the circle"],
                    ["the cross is on the right of the line"]],
                4: [["the square is on the right of the circle"],
                    ["the triangle is on the left of the square"],
                    ["the cross is in front of the triangle"],
                    ["the line is in front of the circle"],
                    ["the triangle is on the right of the circle"]],
                5: [["the circle is on the right of the square"],
                    ["the triangle is on the left of the circle"],
                    ["the cross is in front of the triangle"],
                    ["the line is in front of the square"],
                    ["the cross is on the right of the line"]],
                6: [["the triangle is on the right of the square"],
                    ["the circle is in front of the square"],
                    ["the cross is on the left of the triangle"],
                    ["the line is in front of the cross"],
                    ["the line is on the right of the ell"],
                    ["the star is in front of the ell"],
                    ["the circle is on the left of the vee"],
                    ["the ess is in front of the vee"],
                    ["the star is on the right of the ess"]],
                7: [["the triangle is in front of the square"],
                    ["the circle is on the right of the square"],
                    ["the cross is behind the triangle"],
                    ["the line is on the right of the cross"],
                    ["the line is in front of the ell"],
                    ["the star is on the right of the ell"],
                    ["the circle is behind the vee"],
                    ["the ess is on the right of the vee"],
                    ["the star is in front of the ess"]],
                8: [["the triangle is on top of the square"],
                    ["the circle is on the right of the square"],
                    ["the cross is below the triangle"],
                    ["the line is on the right of the cross"],
                    ["the line is on top of the ell"],
                    ["the star is on the right of the ell"],
                    ["the circle is below the vee"],
                    ["the ess is on the right of the vee"],
                    ["the star is on top of the ess"]]
                },
            # Problems with inconsistent premises
            'inconsistent': {
                1: [["the square is on the left of the circle"],
                    ["the cross is in front of the square"],
                    ["the triangle is on the right of the circle"],
                    ["the triangle is behind the line"],
                    ["the line is on the left of the cross"]],
                2: [["the square is in front of the circle"],
                    ["the triangle is behind the circle"],
                    ["the triangle is in front of the square"]],
                3: [["the triangle is on the right of the square"],
                    ["the circle is in front of the square"],
                    ["the cross is on the left of the square"],
                    ["the line is in front of the cross"],
                    ["the line is on the right of the ell"],
                    ["the star is in front of the ell"],
                    ["the circle is on the left of the vee"],
                    ["the ess is in front of the vee"],
                    ["the star is on the right of the ess"]]
                },
            # 1. Determinate 1D problem, 2: Determinate 2D problem,
            # 3. Prism problem 3
            'generatedet': {
                1: [["the square is in front of the circle"],
                    ["the triangle is behind the circle"],
                    ["what is the relation between the triangle and the square"]],
                2: [["the circle is on the right of the square"],
                    ["the triangle is on the left of the square"],
                    ["the cross is in front of the triangle"],
                    ["the line is in front of the circle"],
                    ["what is the relation between the cross and the line"]],
                3: [["the circle is on the right of the square"],
                    ["the triangle is on the left of the square"],
                    ["the cross is in front of the triangle"],
                    ["the star is in front of the square"],
                    ["what is the relation between the cross and the star"]],
                },
            # 1. Indeterminate 1D problem, 2. Indeterminate 2D problem
            # 3. Prism problem 5, 4. Prism problem 6, 5. Prism problem 7(c)
            'generateindet': {
                1: [["the square is on the right of the circle"],
                    ["the triangle is on the left of the square"],
                    ["what is the relation between the triangle and the circle"]],
                2: [["the square is on the right of the circle"],
                    ["the triangle is on the left of the square"],
                    ["the cross is in front of the triangle"],
                    ["the line is in front of the circle"],
                    ["what is the relation between the cross and the line"]],
                3: [["the square is on the left of the triangle"],
                    ["the circle is on the right of the triangle"],
                    ["the triangle is on the left of the cross"],
                    ["the cross is on the left of the star"],
                    ["what is the relation between the triangle and the star"]],
                4: [["the square is on the right of the triangle"],
                    ["the circle is on the left of the square"],
                    ["the cross is in front of the circle"],
                    ["the star is in front of the square"],
                    ["what is the relation between the circle and the triangle"]],
                5: [["the square is on the right of the triangle"],
                    ["the circle is on the left of the square"],
                    ["the cross is in front of the circle"],
                    ["the star is in front of the triangle"],
                    ["what is the relation between the cross and the star"]]
                },
            'generateall': {
                1: [["the circle is on the left of the square"],
                    ["the triangle is on the right of the square"],
                    ["the cross is behind the triangle"],
                    ["the line is behind the circle"],
                    ["generate all models"]],
                2: [["the square is on the right of the circle"],
                    ["the triangle is on the right of the square"],
                    ["the star is on the right of the triangle"],
                    ["the line is on the right of the star"],
                    ["generate all models"]],
                3: [["the square is on the right of the circle"],
                    ["the triangle is on the left of the square"],
                    ["generate all models"]],
                4: [["the square is on the right of the circle"],
                    ["the triangle is on the left of the square"],
                    ["the cross is in front of the triangle"],
                    ["the star is in front of the circle"],
                    ["generate all models"]],
                5: [["the square is on the left of the triangle"],
                    ["the circle is on the right of the triangle"],
                    ["the triangle is on the left of the cross"],
                    ["the cross is on the left of the ess"],
                    ["generate all models"]],
                6: [["the square is on the right of the circle"],
                    ["the triangle is on the left of the square"],
                    ["the cross is in front of the circle"],
                    ["the line is in front of the triangle"],
                    ["the ell is in front of the triangle"],
                    ["generate all models"]],
                7: [["the square is on the right of the circle"],
                    ["the triangle is on the left of the square"],
                    ["the cross is in front of the circle"],
                    ["the line is in front of the triangle"],
                    ["the ell is in front of the triangle"],
                    ["the ess is in front of the line"],
                    ["generate all models"]],
                8: [["the square is on the left of the circle"],
                    ["the triangle is on the right of the square"],
                    ["the cross is behind the triangle"],
                    ["the star is behind the square"],
                    ["generate all models"]],
                9: [["the square is on the left of the circle"],
                    ["the triangle is on the right of the square"],
                    ["the cross is in front of the triangle"],
                    ["the star is behind the square"],
                    ["generate all models"]],
                10: [["the square is on the right of the triangle"],
                     ["the circle is on the right of the square"],
                     ["the star is on the right of the square"],
                     ["the cross is on the right of the circle"],
                     ["generate all models"]],
                11: [["the square is on the right of the triangle"],
                     ["the circle is on the right of the square"],
                     ["the star is on the left of the square"],
                     ["the cross is on the left of the circle"],
                     ["generate all models"]],
                12: [["the square is on the right of the triangle"],
                     ["the circle is on the right of the square"],
                     ["the star is on the right of the square"],
                     ["the cross is on the right of the square"],
                     ["generate all models"]],
                }
            }
        self.premises = []
        self.models = []

    def test(self, prob_type, num):
        """ This function calls the interpret function with the chosen
        set of premises.
        prob_type: type of problem (as defined in the sample problem types)
        n: key in corresponding dictionary (problem no. of the selected type
        """
        prems = self.problems['combination'][num] if prob_type == 'combination' \
          else self.problems['deductive'][num] if prob_type == 'deductive' \
          else self.problems['inconsistent'][num] if prob_type == 'inconsistent' \
          else self.problems['indeterminate'][num] if prob_type == 'indeterminate' \
          else self.problems['generatedet'][num] if prob_type == 'generatedet'\
          else self.problems['generateindet'][num]

        mods = self.interpret(prems)
#        print("Spatial array data structure at the end:")
#        print(mods[len(mods)-1])
        if prob_type in ['generatedet', 'generateindet']:
            utilities.print_premises(prems[:-1])
        else:
            utilities.print_premises(prems)
        if len(self.models) > 1:
            # Indicates an indeterminate problem: nothing is appended to
            # self.models for a determinate problem.
            spatial_array.print_multiple_mods(self.models, prob_type,
                                              len(self.models))
        else:
            spatial_array.print_array(mods[len(mods)-1], prob_type)

    def interpret(self, prems):
        """ High-level function takes list of premises, parses each one,
        and then applies decide to result, It then calls decide, which uses
        call_appropriate_func to decide whether to start a new model,
        add a subject or an object to an existing model, combine models
        or verify if a conclusion premise (in which all tokens are already
        present in the mental model) has a relation in the model according
        to its intensional representation. Each of the functions including
        verify_model, returns a model. The updated list of mods is returned to
        interpret by decide."""
        self.premises = prems
        #parser = SpatialParser()
        print("Set of premises = {}".format(prems))
        print("Intensional representation of first premise:")
        print(PARSER.parse(prems[0][0]))
        # mods is a list of models. Each individual model is a dict with
        # coordinates as tuple keys. The whole mods list is essentially
        # a history of models at the end of each premise
        mods = []
        for premise in prems:
            mods = self.decide(PARSER.parse(premise[0]), mods)
        return mods

    def decide(self, prop, mods):
        """ This function decides what func to call depending on what is
        already in the mods list of dictionaries. Each mod in mods is a
        separate model. prop (proposition) is a list containing reln, subject
        and object (e.g. [[0, 1, 0], ['[]'], ['O']]).
        find_item is used to check if subj and obj are in mods in 2 separate
        calls, it returns a list containing coords and mod if subj (or obj) is
        present, otherwise it returns None. The extract function extracts the
        model containing subject and object (if a model contains them) from
        the list of mods. It then calls call_appropriate function, which
        decides which functions to call based on if subj and/or obj are in
        mods. """
        #rel = utilities.relfn(prop)
        obj = utilities.objfn(prop)
        subj = utilities.subjfn(prop)
        # Inttialize None and {} for coords and mods. These values are used if
        # find_item does not find subj and/or obj in mods (if it returns None).
        subj_coords = None
        obj_coords = None
        subj_mod = {}
        obj_mod = {}
        # Find subj and obj in mods
        subj_coords_mod = utilities.find_item(subj, mods)
        obj_coords_mod = utilities.find_item(obj, mods)
        if subj_coords_mod is not None:
            subj_coords = subj_coords_mod[0]
            subj_mod = subj_coords_mod[1]
        if obj_coords_mod is not None:
            obj_coords = obj_coords_mod[0]
            obj_mod = obj_coords_mod[1]
        # Extract the mod in which subj/obj were found from the list of mods,
        # this removes the relevant mod from mods. The updated model is
        # appended to model returned by call_appropriate_function.
        mods = utilities.extract(subj_mod, mods)
        mods = utilities.extract(obj_mod, mods)
        # Call call_appropriate_func to, well, call the appropriate function,
        # a model is returned whichever function is called from there. Before
        # that, package up the arguments, as there would be too many to pass
        # without upsetting Pylint.
        coords = (subj_coords, obj_coords)
        models_to_pass = (subj_mod, obj_mod)
        model = self.call_appropriate_func(prop, coords, models_to_pass)
        mods.append(model)
        return mods

    def call_appropriate_func(self, prop, coords, models):
        """ This function calls appropriate functions depending on
        whether subj_coords or obj_coords are already in mods (not None).
        If subj and obj are in models , it calls verify_model. If one of
        them is in mods, it calls add-item (add subj or add object).
        If neither is in models, it calls startmod. If subj_mod
        and obj_mod are mutually independent, it calls combine."""
        # Unpack coords and mods tuples: this is necessary only to prevent
        # Pylint no. of vairables and no. of statements warnings.
        subj_coords, obj_coords = coords
        subj_mod, obj_mod = models
        rel = utilities.relfn(prop)
        subj = utilities.subjfn(prop)
        obj = utilities.objfn(prop)
        if subj_coords is not None and obj_coords is not None:
            if subj_mod == obj_mod:
                # We have reached a conclusion premise, i.e. subj and obj
                # were found in the same mod. OR we need to generate a
                # conclusion if rel = (), empty tuple returned by relfn
                if rel == ():
                    # We have to generate the relation between subj and
                    # obj as we have a generate conclusion current premise
                    rel = model_validation.find_rel_prop(subj_coords,
                                                         obj_coords)
                    prop[0] = list(rel)
                    # Call a function to generate the conclusion and print
                    # it. If the conclusions are different in the preferred
                    # model and in an alternative model, both conclusions are
                    # printed, along with the 2 models.
                    self.gen_and_print_conclusions(prop, subj_mod)
                    return subj_mod
                print("Verifying if the conclusion is correct!")
                mod = model_validation.verify_model(prop, subj_mod)
                if mod is not None:
                    print("Premises are true in model. \nIntermediate model: "
                          "\n{}.\nAttempting to falsify the model."
                          .format(mod))
                    alt_mod = model_validation.make_false(prop, subj_mod,
                                                          self.premises)
                    print("Make false returned mod: \n{}".format(alt_mod))
                    if mod == alt_mod:
                        print("No falsifying model found!\nPremise follows "
                              "validly from previous premises.\nFinal model "
                              "(premises true): {}".format(mod))
                    else:
                        print("Premise was previously possibly true, but can "
                              "also be false.\n Initial model (premises true):"
                              "\n{}\nVaried model (premises false):\n {}\n"
                              .format(mod, alt_mod))
                        self.models.append(mod)
                        self.models.append(alt_mod)
                    return alt_mod
                # verify_model returned None
                print("Premises are false in model.\nIntermediate model: \n{}"
                      "\nAttempting to make the model true.\n".format(subj_mod))
                alt_mod = model_validation.make_true(prop, subj_mod,
                                                     self.premises)
                print("Make true returned mod: \n{}".format(alt_mod))
                if subj_mod == alt_mod:
                    print("No true model found!\nPremise is inconsistent with "
                          "previous premises.\nFinal model (premises false):"
                          "\n{}:\n".format(subj_mod))
                else:
                    print("Premise was previously possibly false, but can also"
                          " be true.\nInitial model (premises false):\n {}\n"
                          "Altered model (premises true):{}\n"
                          .format(subj_mod, alt_mod))
                    self.models.append(subj_mod)
                    self.models.append(alt_mod)
                return subj_mod

            # There are separate subj and obj mods which need to be combined
            # (subj_mod != obj_mod)
            print("Combining 2 separate models together.")
            mod = model_combination.combine(rel, subj_coords, obj_coords,
                                            subj_mod, obj_mod)
            print("Intermediate model: \n{}".format(mod))
            return mod
        elif subj_coords is not None and obj_coords is None:
            print("Adding object!")
            # Subj-obj order interchanged, rel interchanged.
            mod = model_builder.add_item(subj_coords, utilities.convert(rel),
                                         obj, subj_mod)
            print("Intermediate model: \n{}".format(mod))
        elif subj_coords is None and obj_coords is not None:
            print("Adding subject!")
            # Regular 2nd premise, rel unchanged
            mod = model_builder.add_item(obj_coords, rel, subj, obj_mod)
            print("Intermediate model: \n{}".format(mod))
        else:
            print("Starting model")
            mod = model_builder.start_mod(rel, subj, obj)
            print("Intermediate model: \n{}".format(mod))
        # return model: applies for add subj, add obj and start model
        return mod

    def gen_and_print_conclusions(self, prop, mod):
        """ Function which generates the conclusion based on the intensional
        representaiton of the question premise -- prop (obtained from the rel
        between the subject and object in the question, and the model"""
        # Generate the conclusion premise in words from prop.
        conclusion = PARSER.generate_conclusion(prop)
        # Repalce the last premise with the generated conclusion
        self.premises[-1] = [conclusion]
        # For indeterminate problems, there can be more than one
        # model. Get one such model by calling make false
        print("Attempting to falsify the generated conclusion/model.")
        alt_mod = model_validation.make_false(prop, mod,
                                              self.premises)
        if mod != alt_mod:
            print("Different conclusions are found in different"
                  " models")
            print("Conclusion generated in initial model: {}"
                  .format(conclusion))
            print("Initial model: {}".format(mod))
            # Note: make_false negates the relation in prop and
            # changes carry over to the calling function. We don't
            # need to negate the prop again.
            print("Conclusion generated in an altered model:"
                  " {}".format(PARSER.generate_conclusion(prop)))
            print("Altered model: {}".format(alt_mod))
            print("NO VALID CONCLUSION possible!")
            self.models.append(mod)
            self.models.append(alt_mod)
        else:
            print("No alternative conclusions found")
            print("Generated conclusion: {}".format(conclusion))
            print("Final model: {}".format(mod))
            self.models.append(mod)

def main():
    """ Main function which parses the command line, creates objects
    to call the main SpatialReasoning function test. """
    try:
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("category",
                                choices=["combination", "deductive",
                                         "indeterminate", "inconsistent",
                                         "generatedet", "generateindet",
                                         "generateall"],
                                help="Problem category")
        arg_parser.add_argument("n", type=int, help="Sub-problem number")
        args = arg_parser.parse_args()
        reason = SpatialReasoning()
        if args.category == 'generateall':
            print("Looks like you are trying to generate all possible models."
                  " This is not possible in this program which is based on "
                  "Johnson-Laird's Lisp framework. "
                  "Please run prism.py with the same problem.")
            sys.exit(1)
        reason.test(args.category, args.n)
    except KeyError:
        print("Sorry, there is no {} premise number {}".format(args.category,
                                                               args.n))

if __name__ == '__main__':
    main()
