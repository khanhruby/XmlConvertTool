# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "djangoproject/django-box-2.0"
  config.vm.host_name = "djangobox"
  config.ssh.forward_agent = true

  # Shared folders
  utilize_nfs = (/cygwin|mswin|mingw|bccwin|wince|emx/ =~ RUBY_PLATFORM) == nil
  config.vm.synced_folder "../django", "/django", nfs: utilize_nfs

  config.vbguest.auto_update = false

  # do NOT download the iso file from a webserver
  config.vbguest.no_remote = true

  # Host-only network required to use NFS shared folders
  config.vm.network "private_network", ip: "1.2.3.4"

  config.vm.network :forwarded_port, guest: 8000, host: 8000, auto_correct: true
  config.vm.network :forwarded_port, guest: 8001, host: 8001, auto_correct: true
  config.vm.network :forwarded_port, guest: 8002, host: 8002, auto_correct: true
  config.vm.network :forwarded_port, guest: 8003, host: 8003, auto_correct: true
  config.vm.network :forwarded_port, guest: 8004, host: 8004, auto_correct: true
  config.vm.network :forwarded_port, guest: 8005, host: 8005, auto_correct: true
  config.vm.network :forwarded_port, guest: 8006, host: 8006, auto_correct: true
  config.vm.network :forwarded_port, guest: 8007, host: 8007, auto_correct: true
  config.vm.network :forwarded_port, guest: 80, host: 8080, auto_correct: true
end
