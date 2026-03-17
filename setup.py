#!/usr/bin/env python3
"""
Hermes Project Setup Script

This script automates the setup process for the Hermes project,
including Doppler configuration and secret management.

Usage:
    python setup.py                    # Interactive setup
    python setup.py --quick            # Quick setup with defaults
    python setup.py --verify           # Verify existing setup
    python setup.py --list-secrets     # List available secrets
    python setup.py --load <env>       # Load specific environment
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional, List, Dict


class HermesSetup:
    """Automated setup for Hermes project with Doppler integration."""
    
    AVAILABLE_ENVS = ['dev', 'dev_personal', 'stg', 'prd']
    DEFAULT_ENV = 'dev'
    
    def __init__(self, project_dir: Optional[Path] = None):
        self.project_dir = project_dir or Path.cwd()
        self.doppler_installed = False
        self.doppler_authenticated = False
        
    def log(self, message: str, level: str = 'info'):
        """Print formatted log messages."""
        prefixes = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'step': '📋'
        }
        prefix = prefixes.get(level, 'ℹ️')
        print(f"[{prefix}] {message}")
        
    def check_doppler_cli(self) -> bool:
        """Check if Doppler CLI is installed."""
        self.log("Checking Doppler CLI installation...", "step")
        try:
            result = subprocess.run(
                ['doppler', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                self.doppler_installed = True
                self.log(f"Doppler CLI is installed: {result.stdout.strip()}", "success")
                return True
            else:
                self.log("Doppler CLI is not installed or not accessible", "error")
                return False
        except FileNotFoundError:
            self.log("Doppler CLI not found in PATH", "error")
            return False
        except Exception as e:
            self.log(f"Error checking Doppler CLI: {e}", "error")
            return False
            
    def check_auth(self) -> bool:
        """Check if user is authenticated with Doppler."""
        if not self.doppler_installed:
            return False
            
        self.log("Checking Doppler authentication...", "step")
        try:
            result = subprocess.run(
                ['doppler', 'whoami'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                self.doppler_authenticated = True
                self.log("Successfully authenticated with Doppler", "success")
                return True
            else:
                self.log("Not authenticated with Doppler", "error")
                return False
        except Exception as e:
            self.log(f"Error checking authentication: {e}", "error")
            return False
            
    def login_doppler(self) -> bool:
        """Interactive Doppler login."""
        self.log("Starting Doppler login...", "step")
        self.log("Please follow the prompts to authenticate.", "info")
        
        try:
            result = subprocess.run(
                ['doppler', 'login'],
                capture_output=False,
                text=True,
                timeout=120
            )
            if result.returncode == 0:
                self.doppler_authenticated = True
                self.log("Login successful!", "success")
                return True
            else:
                self.log("Login failed", "error")
                return False
        except Exception as e:
            self.log(f"Login error: {e}", "error")
            return False
            
    def verify_hermes_project(self) -> bool:
        """Verify Hermes project configuration exists."""
        self.log("Verifying Hermes project configuration...", "step")
        
        try:
            result = subprocess.run(
                ['doppler', 'configs', '--project', 'hermes'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                # Check if 'hermes' appears in output
                if 'hermes' in result.stdout.lower():
                    self.log("Hermes project found!", "success")
                    return True
                else:
                    self.log("Project verification inconclusive", "warning")
                    return True  # Still proceed, might be permissions issue
            else:
                self.log("Could not verify Hermes project", "error")
                return False
        except Exception as e:
            self.log(f"Error verifying project: {e}", "error")
            return False
            
    def list_environments(self) -> List[str]:
        """List available Doppler environments for Hermes project."""
        if not (self.doppler_installed and self.doppler_authenticated):
            return []
            
        self.log("Fetching available environments...", "step")
        
        try:
            result = subprocess.run(
                ['doppler', 'configs', '--project', 'hermes'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Parse environment names from output
                lines = result.stdout.strip().split('\n')
                envs = []
                for line in lines:
                    if 'hermes' in line.lower():
                        parts = line.split()
                        for part in parts:
                            # Look for environment names (dev, stg, prd, etc.)
                            if part in self.AVAILABLE_ENVS:
                                envs.append(part)
                return list(set(envs)) if envs else self.AVAILABLE_ENVS
            else:
                self.log("Could not fetch environments", "warning")
                return self.AVAILABLE_ENVS
                
        except Exception as e:
            self.log(f"Error listing environments: {e}", "error")
            return self.AVAILABLE_ENVS
            
    def load_secrets(self, env: str, format: str = 'env') -> bool:
        """Load secrets from Doppler for specified environment."""
        if not (self.doppler_installed and self.doppler_authenticated):
            return False
            
        self.log(f"Loading secrets for '{env}' environment...", "step")
        
        try:
            # Create output file
            output_file = self.project_dir / f'.env.{env}'
            
            result = subprocess.run(
                [
                    'doppler', 'secrets', 'download',
                    '--config', env,
                    '--project', 'hermes',
                    f'--format={format}',
                    '--no-file'
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Write secrets to file
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
                
                self.log(f"Secrets downloaded to {output_file.name}", "success")
                return True
            else:
                self.log(f"Failed to download secrets: {result.stderr}", "error")
                return False
                
        except Exception as e:
            self.log(f"Error loading secrets: {e}", "error")
            return False
            
    def get_secrets_json(self, env: str) -> Optional[Dict]:
        """Get secrets as JSON for inspection."""
        if not (self.doppler_installed and self.doppler_authenticated):
            return None
            
        try:
            result = subprocess.run(
                [
                    'doppler', 'secrets', 'download',
                    '--config', env,
                    '--project', 'hermes',
                    '--format=json',
                    '--no-file'
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                self.log(f"Error fetching secrets: {result.stderr}", "error")
                return None
                
        except json.JSONDecodeError as e:
            self.log(f"Error parsing JSON: {e}", "error")
            return None
        except Exception as e:
            self.log(f"Error getting secrets: {e}", "error")
            return None
            
    def test_connection(self, env: str) -> bool:
        """Test that secrets are properly loaded."""
        self.log("Testing Doppler connection...", "step")
        
        try:
            result = subprocess.run(
                [
                    'doppler', 'run',
                    '--config', env,
                    '--project', 'hermes',
                    '--',
                    'env', '|', 'grep', '-E', '(DOPPLER|API)'
                ],
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Try alternative approach
            test_cmd = f'doppler run --config {env} --project hermes -- sh -c "echo $DOPPLER_CONFIG"'
            result = subprocess.run(
                test_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and 'hermes' in result.stdout.lower():
                self.log("Connection test successful!", "success")
                return True
            else:
                self.log("Connection test failed", "error")
                return False
                
        except Exception as e:
            self.log(f"Error during connection test: {e}", "error")
            return False
            
    def quick_setup(self):
        """Run quick setup with minimal interaction."""
        self.log("=" * 60, "step")
        self.log("HERMES PROJECT - QUICK SETUP", "step")
        self.log("=" * 60, "step")
        
        # Check prerequisites
        if not self.check_doppler_cli():
            self.log("Installing Doppler CLI required", "error")
            self.log("See SETUP_GUIDE.md for installation instructions", "info")
            return False
            
        if not self.check_auth():
            self.log("Authentication required", "warning")
            if not self.login_doppler():
                return False
                
        # Verify project
        if not self.verify_hermes_project():
            self.log("Project verification failed", "warning")
            
        # Load default environment
        envs = self.list_environments()
        self.log(f"Found environments: {', '.join(envs)}", "info")
        
        if self.DEFAULT_ENV in envs:
            if self.load_secrets(self.DEFAULT_ENV):
                if self.test_connection(self.DEFAULT_ENV):
                    self.log("=" * 60, "success")
                    self.log("SETUP COMPLETE!", "success")
                    self.log(f"Use 'doppler run --config {self.DEFAULT_ENV} --project hermes -- <command>' to run with secrets", "info")
                    self.log("=" * 60, "success")
                    return True
        else:
            self.log("No valid environments found", "error")
            
        return False
        
    def interactive_setup(self):
        """Run interactive setup with user prompts."""
        self.log("=" * 60, "step")
        self.log("HERMES PROJECT - INTERACTIVE SETUP", "step")
        self.log("=" * 60, "step")
        
        # Check prerequisites
        if not self.check_doppler_cli():
            self.log("\n❌ Doppler CLI not found", "error")
            self.log("\nTo install Doppler CLI:", "info")
            self.log("  - macOS: brew install doppler", "info")
            self.log("  - Ubuntu: curl -L https://packagecloud.io/install/repositories/dopplerhq/doppler/script.deb.sh | sudo bash && sudo apt-get install doppler", "info")
            self.log("  - Or download from: https://doppler.com/docs/cli", "info")
            return False
            
        if not self.check_auth():
            self.log("\n⚠️  Not authenticated with Doppler", "warning")
            if not self.login_doppler():
                return False
                
        # Verify project
        if not self.verify_hermes_project():
            self.log("\n⚠️  Could not verify Hermes project", "warning")
            
        # List environments
        envs = self.list_environments()
        self.log(f"\n📋 Available environments: {', '.join(envs)}", "info")
        
        # Ask which environment to load
        print("\nWhich environment would you like to load?")
        for i, env in enumerate(envs, 1):
            marker = " ← default" if env == self.DEFAULT_ENV else ""
            print(f"  {i}. {env}{marker}")
            
        choice = input("\nEnter choice (1): ").strip() or "1"
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(envs):
                selected_env = envs[choice_num - 1]
            else:
                selected_env = self.DEFAULT_ENV
        except ValueError:
            selected_env = self.DEFAULT_ENV
            
        self.log(f"\n📦 Loading secrets for '{selected_env}'...", "step")
        
        if self.load_secrets(selected_env):
            if self.test_connection(selected_env):
                self.log("\n" + "=" * 60, "success")
                self.log("✅ SETUP COMPLETE!", "success")
                self.log("=" * 60, "success")
                self.log(f"\nRun commands with secrets loaded:", "info")
                self.log(f"  doppler run --config {selected_env} --project hermes -- <your-command>")
                self.log(f"\nExample:", "info")
                self.log(f"  doppler run --config {selected_env} --project hermes -- python app.py")
                self.log("\nSecrets file created:", "info")
                self.log(f"  .env.{selected_env}")
                self.log("=" * 60, "success")
                return True
                
        self.log("\n❌ Setup failed", "error")
        return False
        
    def verify_setup(self):
        """Verify current setup status."""
        self.log("=" * 60, "step")
        self.log("HERMES PROJECT - SETUP VERIFICATION", "step")
        self.log("=" * 60, "step")
        
        # Check Doppler CLI
        self.log("\n📦 Doppler CLI Status:", "step")
        cli_status = self.check_doppler_cli()
        self.log(f"  {'✅ Installed' if cli_status else '❌ Not installed'}", "info")
        
        # Check authentication
        self.log("\n🔐 Authentication Status:", "step")
        auth_status = self.check_auth()
        self.log(f"  {'✅ Authenticated' if auth_status else '❌ Not authenticated'}", "info")
        
        # Verify project
        self.log("\n📁 Project Status:", "step")
        project_status = self.verify_hermes_project()
        self.log(f"  {'✅ Found' if project_status else '❌ Not found'}", "info")
        
        # List environments
        if auth_status:
            envs = self.list_environments()
            self.log(f"\n🌍 Available Environments: {', '.join(envs) if envs else 'None found'}", "step")
            
            # Check for existing env files
            self.log("\n💾 Local Secret Files:", "step")
            for env in envs:
                env_file = self.project_dir / f'.env.{env}'
                if env_file.exists():
                    size = env_file.stat().st_size
                    self.log(f"  ✅ .env.{env} ({size} bytes)", "info")
                else:
                    self.log(f"  ❌ .env.{env} (not found)", "warning")
                    
            # Test default environment
            if self.DEFAULT_ENV in envs:
                self.log(f"\n🧪 Testing '{self.DEFAULT_ENV}' environment:", "step")
                test_status = self.test_connection(self.DEFAULT_ENV)
                self.log(f"  {'✅ Connection OK' if test_status else '❌ Connection failed'}", "info")
                
        else:
            self.log("\n⚠️  Authentication required to list environments", "warning")
            
        self.log("\n" + "=" * 60, "step")
        self.log("VERIFICATION COMPLETE", "step")
        self.log("=" * 60, "step")
        
        # Provide next steps
        if not cli_status:
            self.log("\n📖 Next steps:", "info")
            self.log("  1. Install Doppler CLI (see SETUP_GUIDE.md)", "info")
        elif not auth_status:
            self.log("\n📖 Next steps:", "info")
            self.log("  1. Run: doppler login", "info")
            self.log("  2. Follow the authentication prompts", "info")
        else:
            self.log("\n📖 Next steps:", "info")
            self.log(f"  1. Run commands with: doppler run --config {self.DEFAULT_ENV} --project hermes -- <command>", "info")
            
    def list_secrets(self):
        """List all secrets for specified environment."""
        self.log("=" * 60, "step")
        self.log("HERMES PROJECT - SECRETS LIST", "step")
        self.log("=" * 60, "step")
        
        if not (self.doppler_installed and self.doppler_authenticated):
            self.log("Authentication required", "error")
            return False
            
        # Try to list secrets
        try:
            result = subprocess.run(
                ['doppler', 'secrets', 'ls', '--project', 'hermes', '--config', self.DEFAULT_ENV],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(result.stdout)
                return True
            else:
                self.log(f"Error listing secrets: {result.stderr}", "error")
                return False
                
        except Exception as e:
            self.log(f"Error: {e}", "error")
            return False
            
    def load_environment(self, env: str):
        """Load a specific environment."""
        if env not in self.AVAILABLE_ENVS:
            self.log(f"Invalid environment: {env}", "error")
            self.log(f"Available: {', '.join(self.AVAILABLE_ENVS)}", "info")
            return False
            
        if not (self.doppler_installed and self.doppler_authenticated):
            self.log("Authentication required", "error")
            return False
            
        self.log(f"Loading environment: {env}", "step")
        
        if self.load_secrets(env):
            self.log(f"✅ Successfully loaded {env} environment", "success")
            return True
        else:
            self.log(f"❌ Failed to load {env} environment", "error")
            return False


def main():
    """Main entry point."""
    setup = HermesSetup()
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    if not args or '--help' in args or '-h' in args:
        print(__doc__)
        print("\nExamples:")
        print("  python setup.py                    # Interactive setup")
        print("  python setup.py --quick            # Quick setup with defaults")
        print("  python setup.py --verify           # Verify existing setup")
        print("  python setup.py --list-secrets     # List available secrets")
        print("  python setup.py --load stg         # Load staging environment")
        print()
        return
    
    # Handle different commands
    if '--quick' in args:
        success = setup.quick_setup()
        sys.exit(0 if success else 1)
        
    elif '--verify' in args:
        setup.verify_setup()
        sys.exit(0)
        
    elif '--list-secrets' in args:
        setup.list_secrets()
        sys.exit(0 if setup.doppler_installed and setup.doppler_authenticated else 1)
        
    elif '--load' in args:
        env_index = args.index('--load')
        if env_index + 1 < len(args):
            env = args[env_index + 1]
            setup.load_environment(env)
            sys.exit(0)
        else:
            print("Error: --load requires an environment name", file=sys.stderr)
            sys.exit(1)
            
    # Default: interactive setup
    else:
        success = setup.interactive_setup()
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
