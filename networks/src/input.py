#
# Copyright (C) 2021 Dalisha Logan <https://www.cms-labs.org/people/dalisha.logan/>
# Copyright (C) 2021 Tobias Hardes <https://www.cms-labs.org/people/hardes/>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


import sys


def check_numbers_valid(prompt, *args):
    "Checks whether the input contains some special characters."

    special_characters = "!@#$%^&*()-+?_=,<>/"

    if special_characters in str(prompt):
        sys.exit("Input contains special characters.")

    # Check whether a float or an integer value must be returned
    try:
        f = float(prompt)
        i = int(f)

        if f != i:
            if len(args) != 0:
                prompt = round(f, 2)
            else:
                sys.exit('Please enter Integers.')
        else:
            prompt = i

    except ValueError:
        sys.exit("Please enter Integers or Floats.")

    return prompt
